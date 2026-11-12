from decimal import Decimal

from django.core.management.base import BaseCommand

from catalogo.models import Producto

# (nombre, descripción, categoría, precio, stock, disponible, imagen)
DATOS = [
    ('laptop lenovo ideapad', 'Laptop de 15.6" con 16 GB RAM y SSD de 512 GB.', 'tecnologia', '2599.90', 8, True, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=70'),
    ('mouse inalámbrico logitech', 'Mouse ergonómico con conexión USB.', 'tecnologia', '59.50', 25, True, 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=70'),
    ('teclado mecánico redragon', 'Teclado mecánico retroiluminado.', 'tecnologia', '189.00', 4, True, 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=70'),
    ('audífonos bluetooth sony', 'Audífonos con cancelación de ruido.', 'tecnologia', '349.00', 0, False, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=70'),
    ('lámpara de escritorio led', 'Lámpara regulable con puerto USB.', 'hogar', '45.00', 15, True, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=70'),
    ('juego de sábanas queen', 'Sábanas de algodón 200 hilos.', 'hogar', '120.00', 3, True, 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=70'),
    ('silla ergonómica de oficina', 'Silla con soporte lumbar y ruedas.', 'oficina', '429.90', 6, True, 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?auto=format&fit=crop&w=800&q=70'),
    ('cuaderno universitario a4', 'Cuaderno de 100 hojas cuadriculado.', 'oficina', '8.50', 120, True, 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=800&q=70'),
    ('pelota de fútbol n°5', 'Pelota oficial de entrenamiento.', 'deporte', '75.00', 12, True, 'https://images.unsplash.com/photo-1614632537190-23e4146777db?auto=format&fit=crop&w=800&q=70'),
    ('mancuernas ajustables 20 kg', 'Par de mancuernas con discos intercambiables.', 'deporte', '210.00', 2, True, 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=800&q=70'),
]


class Command(BaseCommand):
    help = 'Puebla (o actualiza) la base de datos con los productos de ejemplo.'

    def add_arguments(self, parser):
        parser.add_argument('--limpiar', action='store_true',
                            help='Elimina los productos que no estén en esta lista.')

    def handle(self, *args, **options):
        if options['limpiar']:
            borrados, _ = Producto.objects.exclude(nombre__in=[d[0] for d in DATOS]).delete()
            self.stdout.write(f'{borrados} productos eliminados.')
        nuevos = 0
        for nombre, desc, cat, precio, stock, disp, img in DATOS:
            _, creado = Producto.objects.update_or_create(
                nombre=nombre,
                defaults=dict(descripcion=desc, categoria=cat, precio=Decimal(precio),
                              stock=stock, disponible=disp, imagen_url=img),
            )
            nuevos += int(creado)
        self.stdout.write(self.style.SUCCESS(
            f'{nuevos} productos nuevos ({Producto.objects.count()} en total).'))
