import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from . import cuestionario
from .models import Animal, Evento, Solicitud, SolicitudAdopcion

MEDIA_TEMPORAL = tempfile.mkdtemp()


def tearDownModule():
    shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)


def foto_de_prueba(ancho=3000, alto=2000):
    buffer = BytesIO()
    Image.new('RGB', (ancho, alto), 'purple').save(buffer, format='PNG')
    return SimpleUploadedFile('perrita.png', buffer.getvalue(), content_type='image/png')


class SolicitudPermisosTests(APITestCase):
    def setUp(self):
        self.solicitud = Solicitud.objects.create(
            tipo='ADOPCION', nombre='Ana', email='ana@example.com', telefono='600000000'
        )
        self.url_lista = '/api/solicitudes/'
        self.url_detalle = f'/api/solicitudes/{self.solicitud.id}/'

    def test_publico_puede_crear(self):
        datos = {'tipo': 'VOLUNTARIADO', 'nombre': 'Jon', 'email': 'jon@example.com',
                 'telefono': '611111111', 'gestionada': True}
        respuesta = self.client.post(self.url_lista, datos)
        self.assertEqual(respuesta.status_code, 201)
        self.assertFalse(Solicitud.objects.get(nombre='Jon').gestionada)

    def test_publico_no_puede_leer_ni_borrar(self):
        self.assertEqual(self.client.get(self.url_lista).status_code, 403)
        self.assertEqual(self.client.get(self.url_detalle).status_code, 403)
        self.assertEqual(self.client.delete(self.url_detalle).status_code, 403)
        self.assertTrue(Solicitud.objects.filter(id=self.solicitud.id).exists())

    def test_staff_puede_leer(self):
        admin = User.objects.create_user('admin', password='x', is_staff=True)
        self.client.force_authenticate(admin)
        self.assertEqual(self.client.get(self.url_lista).status_code, 200)


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class AnimalGestionTests(APITestCase):
    def setUp(self):
        self.staff = User.objects.create_user('refugio', password='clave-segura-123', is_staff=True)
        self.animal = Animal.objects.create(nombre='Txuri', descripcion='Muy cariñosa')

    def test_publico_puede_ver_pero_no_cambiar(self):
        self.assertEqual(self.client.get('/api/animales/').status_code, 200)
        self.assertEqual(self.client.post('/api/animales/', {'nombre': 'X', 'descripcion': 'Y'}).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/animales/{self.animal.id}/').status_code, 403)

    def test_usuario_no_staff_no_puede_cambiar(self):
        normal = User.objects.create_user('vecino', password='x')
        self.client.force_authenticate(normal)
        respuesta = self.client.patch(f'/api/animales/{self.animal.id}/', {'estado': 'ADOPTADO'})
        self.assertEqual(respuesta.status_code, 403)

    def test_staff_crea_animal_y_la_foto_se_optimiza(self):
        self.client.force_authenticate(self.staff)
        respuesta = self.client.post('/api/animales/', {
            'nombre': 'Beltza', 'descripcion': 'Gato negro', 'estado': 'URGENTE', 'foto': foto_de_prueba(),
        }, format='multipart')
        self.assertEqual(respuesta.status_code, 201)
        animal = Animal.objects.get(nombre='Beltza')
        self.assertTrue(animal.foto.name.endswith('.jpg'))
        with Image.open(animal.foto.path) as imagen:
            self.assertEqual(max(imagen.size), 1600)

    def test_cambiar_foto_borra_la_anterior(self):
        self.client.force_authenticate(self.staff)
        url = f'/api/animales/{self.animal.id}/'
        self.client.patch(url, {'foto': foto_de_prueba()}, format='multipart')
        self.animal.refresh_from_db()
        foto_vieja = self.animal.foto.name
        self.client.patch(url, {'foto': foto_de_prueba()}, format='multipart')
        self.assertFalse(self.animal.foto.storage.exists(foto_vieja))

    def test_login_y_logout(self):
        self.assertIsNone(self.client.get('/api/auth/sesion/').data['usuario'])
        malo = self.client.post('/api/auth/login/', {'usuario': 'refugio', 'contrasena': 'mal'})
        self.assertEqual(malo.status_code, 400)
        bueno = self.client.post('/api/auth/login/', {'usuario': 'refugio', 'contrasena': 'clave-segura-123'})
        self.assertEqual(bueno.data['usuario'], 'refugio')
        self.assertEqual(self.client.get('/api/auth/sesion/').data['usuario'], 'refugio')
        self.client.post('/api/auth/logout/')
        self.assertIsNone(self.client.get('/api/auth/sesion/').data['usuario'])

    def test_login_rechaza_usuarios_que_no_son_staff(self):
        User.objects.create_user('vecino', password='clave-segura-123')
        respuesta = self.client.post('/api/auth/login/', {'usuario': 'vecino', 'contrasena': 'clave-segura-123'})
        self.assertEqual(respuesta.status_code, 400)


class FlujoNavegadorTests(APITestCase):
    """Como el navegador: con comprobación CSRF activada, igual que en producción."""
    def setUp(self):
        User.objects.create_user('refugio', password='clave-segura-123', is_staff=True)
        self.animal = Animal.objects.create(nombre='Txuri', descripcion='Muy cariñosa')
        self.client = self.client_class(enforce_csrf_checks=True)

    def test_login_y_cambios_con_token_csrf(self):
        self.client.get('/api/auth/sesion/')
        token = self.client.cookies['csrftoken'].value
        respuesta = self.client.post('/api/auth/login/', {'usuario': 'refugio', 'contrasena': 'clave-segura-123'},
                                     HTTP_X_CSRFTOKEN=token)
        self.assertEqual(respuesta.status_code, 200)

        # Al hacer login Django renueva el token: el frontend lee siempre la cookie actual
        token = self.client.cookies['csrftoken'].value
        url = f'/api/animales/{self.animal.id}/'
        self.assertEqual(self.client.patch(url, {'estado': 'ADOPTADO'}).status_code, 403)
        self.assertEqual(self.client.patch(url, {'estado': 'ADOPTADO'}, HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(self.client.post('/api/auth/logout/', HTTP_X_CSRFTOKEN=token).status_code, 200)


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class EventoGestionTests(APITestCase):
    def setUp(self):
        self.staff = User.objects.create_user('refugio', password='x', is_staff=True)
        self.datos = {'titulo': 'Mercadillo solidario', 'fecha': '2026-12-12', 'horario': 'De 11:00 a 14:00',
                      'lugar': 'Plaza de Sondika', 'descripcion': 'Venta de bitxis para el refugio'}

    def test_publico_puede_ver_pero_no_crear(self):
        self.assertEqual(self.client.get('/api/eventos/').status_code, 200)
        self.assertEqual(self.client.post('/api/eventos/', self.datos).status_code, 403)

    def test_staff_crea_evento_sin_imagen(self):
        self.client.force_authenticate(self.staff)
        respuesta = self.client.post('/api/eventos/', self.datos, format='multipart')
        self.assertEqual(respuesta.status_code, 201)
        self.assertIsNone(respuesta.data['imagen'])

    def test_quitar_imagen_borra_el_archivo(self):
        self.client.force_authenticate(self.staff)
        creado = self.client.post('/api/eventos/', {**self.datos, 'imagen': foto_de_prueba(1000, 1500)}, format='multipart')
        evento = Evento.objects.get(id=creado.data['id'])
        archivo = evento.imagen.name
        self.assertTrue(evento.imagen.storage.exists(archivo))

        respuesta = self.client.patch(f'/api/eventos/{evento.id}/', {'imagen': ''}, format='multipart')
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsNone(respuesta.data['imagen'])
        self.assertFalse(evento.imagen.storage.exists(archivo))


def respuestas_obligatorias(especie):
    respuestas = {p['clave']: 'Respuesta de prueba' for p in cuestionario.preguntas(especie) if p['obligatoria']}
    respuestas.update(nombre='Ane Etxebarria', email='ane@example.com', telefono='600 000 000')
    return respuestas


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class SolicitudAdopcionTests(APITestCase):
    url = '/api/solicitudes-adopcion/'

    def setUp(self):
        self.gata = Animal.objects.create(nombre='Txuri', especie='GATO', descripcion='Muy cariñosa')

    def enviar(self, **cambios):
        datos = {'animal': self.gata.id, 'acepta_privacidad': True, 'respuestas': respuestas_obligatorias('GATO')}
        datos.update(cambios)
        return self.client.post(self.url, datos, format='json')

    def test_cuestionario_publico_por_especie(self):
        perro = self.client.get('/api/cuestionario/perro/').data
        gato = self.client.get('/api/cuestionario/GATO/').data
        claves_gato = [p['clave'] for s in gato['secciones'] for p in s['preguntas']]
        self.assertIn('arenero', claves_gato)
        self.assertNotIn('arenero', [p['clave'] for s in perro['secciones'] for p in s['preguntas']])
        self.assertEqual(self.client.get('/api/cuestionario/conejo/').status_code, 404)

    def test_envio_guarda_la_solicitud_y_manda_el_pdf(self):
        respuestas = {**respuestas_obligatorias('GATO'), 'pregunta_inventada': 'x', 'estado_civil': '  '}
        respuesta = self.enviar(respuestas=respuestas)
        self.assertEqual(respuesta.status_code, 201)

        solicitud = SolicitudAdopcion.objects.get()
        self.assertEqual((solicitud.nombre_animal, solicitud.especie), ('Txuri', 'GATO'))
        self.assertEqual(solicitud.email, 'ane@example.com')
        self.assertNotIn('pregunta_inventada', solicitud.respuestas)
        self.assertNotIn('estado_civil', solicitud.respuestas)
        self.assertFalse(solicitud.gestionada)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ['ane@example.com'])
        nombre, contenido, tipo = mail.outbox[0].attachments[0]
        self.assertEqual(tipo, 'application/pdf')
        self.assertTrue(contenido.startswith(b'%PDF'))

    def test_faltan_obligatorias_o_privacidad(self):
        respuestas = respuestas_obligatorias('GATO')
        del respuestas['dni']
        respuesta = self.enviar(respuestas=respuestas)
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('dni', respuesta.data['respuestas'])

        self.assertEqual(self.enviar(acepta_privacidad=False).status_code, 400)
        self.assertEqual(self.enviar(respuestas={**respuestas_obligatorias('GATO'), 'email': 'no-es-email'}).status_code, 400)
        self.assertFalse(SolicitudAdopcion.objects.exists())

    def test_publico_no_puede_leer_ni_descargar(self):
        self.enviar()
        solicitud = SolicitudAdopcion.objects.get()
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(self.client.get(f'{self.url}{solicitud.id}/pdf/').status_code, 403)

    def test_staff_ve_descarga_y_marca_gestionada(self):
        self.enviar()
        solicitud = SolicitudAdopcion.objects.get()
        self.client.force_authenticate(User.objects.create_user('refugio', password='x', is_staff=True))

        self.assertEqual(len(self.client.get(self.url).data), 1)
        pdf = self.client.get(f'{self.url}{solicitud.id}/pdf/')
        self.assertEqual(pdf['Content-Type'], 'application/pdf')
        self.assertTrue(pdf.content.startswith(b'%PDF'))

        # Solo se puede cambiar "gestionada"; las respuestas no se tocan
        self.client.patch(f'{self.url}{solicitud.id}/', {'gestionada': True, 'nombre': 'Otra'}, format='json')
        solicitud.refresh_from_db()
        self.assertTrue(solicitud.gestionada)
        self.assertEqual(solicitud.nombre, 'Ane Etxebarria')

    def test_borrar_el_animal_conserva_la_solicitud(self):
        self.enviar()
        self.gata.delete()
        solicitud = SolicitudAdopcion.objects.get()
        self.assertIsNone(solicitud.animal)
        self.assertEqual(solicitud.nombre_animal, 'Txuri')
