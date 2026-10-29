import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from .models import Animal, Solicitud

MEDIA_TEMPORAL = tempfile.mkdtemp()


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
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

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
