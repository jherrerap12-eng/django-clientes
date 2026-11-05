from django.test import TestCase
from django.urls import reverse

from .models import Cliente


class ClientesTests(TestCase):
    def registrar(self):
        return self.client.post(reverse('registro'), {
            'username': 'prueba',
            'email': 'prueba@example.com',
            'password1': 'ClaveSegura123',
            'password2': 'ClaveSegura123',
        })

    def test_clientes_pide_sesion(self):
        respuesta = self.client.get(reverse('clientes_crear'))
        self.assertRedirects(respuesta, f"{reverse('login')}?next={reverse('clientes_crear')}")

    def test_flujo_completo(self):
        self.assertRedirects(self.registrar(), reverse('home'))

        respuesta = self.client.post(reverse('clientes_crear'), {
            'nombre': 'Ana',
            'correo': 'ana@example.com',
        }, follow=True)
        self.assertContains(respuesta, 'Cliente guardado: Ana (ana@example.com)')
        self.assertEqual(Cliente.objects.count(), 1)

        repetido = self.client.post(reverse('clientes_crear'), {
            'nombre': 'Otra',
            'correo': 'ana@example.com',
        })
        self.assertEqual(repetido.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 1)

        self.client.post(reverse('logout'))
        self.assertEqual(self.client.get(reverse('clientes_crear')).status_code, 302)

    def test_login_y_recuperar(self):
        self.registrar()
        self.client.post(reverse('logout'))
        respuesta = self.client.post(reverse('login'), {
            'username': 'prueba',
            'password': 'ClaveSegura123',
        })
        self.assertRedirects(respuesta, reverse('home'))
        respuesta = self.client.post(reverse('password_reset'), {'email': 'prueba@example.com'})
        self.assertRedirects(respuesta, reverse('password_reset_done'))
