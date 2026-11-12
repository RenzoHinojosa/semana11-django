from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Producto


class ProductoTests(TestCase):
    def setUp(self):
        Producto.objects.create(nombre='Mouse', precio=Decimal('50'), stock=3, categoria='tecnologia')
        Producto.objects.create(nombre='Silla', precio=Decimal('300'), stock=10, categoria='oficina', disponible=False)

    def test_str(self):
        self.assertEqual(str(Producto.objects.get(nombre='Mouse')), 'Mouse (S/ 50.00)')

    def test_stock_bajo(self):
        self.assertTrue(Producto.objects.get(nombre='Mouse').stock_bajo)
        self.assertFalse(Producto.objects.get(nombre='Silla').stock_bajo)

    def test_filter(self):
        self.assertEqual(Producto.objects.filter(disponible=True).count(), 1)

    def test_home(self):
        r = self.client.get(reverse('catalogo:home'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Bienvenido')

    def test_catalogo_y_filtro(self):
        r = self.client.get(reverse('catalogo:catalogo'))
        self.assertEqual(len(r.context['productos']), 2)
        r = self.client.get(reverse('catalogo:catalogo'), {'categoria': 'oficina'})
        self.assertEqual(len(r.context['productos']), 1)

    def test_busqueda_sin_tildes_ni_plural(self):
        Producto.objects.create(nombre='Audífonos JBL Tune', precio=Decimal('179'), stock=9)
        url = reverse('catalogo:catalogo')
        for consulta in ('audifono', 'AUDIFONOS', 'audífono jbl', 'jbl tune'):
            r = self.client.get(url, {'q': consulta})
            self.assertEqual(len(r.context['productos']), 1, consulta)
        self.assertEqual(len(self.client.get(url, {'q': 'zzz'}).context['productos']), 0)
