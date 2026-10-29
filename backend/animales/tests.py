from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Solicitud


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
