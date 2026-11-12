import unicodedata

from django.db import models


class Producto(models.Model):
    """Producto del catálogo (persistido con el ORM de Django en SQLite)."""

    CATEGORIAS = [
        ('tecnologia', 'Tecnología'),
        ('hogar', 'Hogar'),
        ('oficina', 'Oficina'),
        ('deporte', 'Deporte'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='tecnologia')
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen_url = models.URLField(blank=True, help_text='URL de la imagen del producto')
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return f'{self.nombre} (S/ {self.precio})'

    @property
    def stock_bajo(self):
        """Regla de negocio en el modelo, no en la vista."""
        return self.stock <= 5

    
    CLAVES_FOTO = [
        ('mouse pad', 'mousepad'), ('mouse', 'computer,mouse'), ('laptop', 'laptop'), ('teclado', 'keyboard'),
        ('audifono', 'headphones'), ('parlante', 'speaker'), ('smartwatch', 'smartwatch'), ('tablet', 'tablet'),
        ('monitor', 'monitor'), ('webcam', 'webcam'), ('ssd', 'ssd'), ('usb', 'usb'), ('cargador', 'charger'),
        ('power bank', 'powerbank'), ('router', 'router'), ('smartphone', 'smartphone'), ('microfono', 'microphone'),
        ('impresora', 'printer'), ('camara', 'security,camera'), ('lampara', 'desk,lamp'), ('sabana', 'bedroom'),
        ('licuadora', 'blender'), ('cafetera', 'coffee,machine'), ('freidora', 'air,fryer'), ('olla', 'cookware'),
        ('almohada', 'pillow'), ('aspiradora', 'robot,vacuum'), ('ventilador', 'fan'), ('toalla', 'towels'),
        ('silla', 'office,chair'), ('escritorio de madera', 'desk'), ('organizador', 'desk,organizer'),
        ('soporte', 'laptop,stand'), ('pizarra', 'whiteboard'), ('calculadora', 'calculator'),
        ('resaltador', 'highlighter'), ('archivador', 'filing,cabinet'), ('mochila', 'backpack'),
        ('cuaderno', 'notebook'), ('zapatilla', 'running,shoes'), ('bicicleta', 'mountain,bike'),
        ('colchoneta', 'yoga,mat'), ('casco', 'bike,helmet'), ('polera', 'sportswear'), ('basquet', 'basketball'),
        ('cuerda', 'jump,rope'), ('botella', 'water,bottle'), ('pelota', 'soccer,ball'), ('mancuerna', 'dumbbell'),
    ]
    CLAVES_CATEGORIA = {'tecnologia': 'technology', 'hogar': 'furniture', 'oficina': 'office', 'deporte': 'sport'}

    @property
    def imagen_respaldo(self):
        """Foto alternativa (por palabra clave) si la imagen principal no carga."""
        nombre = ''.join(c for c in unicodedata.normalize('NFD', self.nombre.lower())
                         if unicodedata.category(c) != 'Mn')
        clave = next((k for palabra, k in self.CLAVES_FOTO if palabra in nombre),
                     self.CLAVES_CATEGORIA.get(self.categoria, 'product'))
        return f'https://loremflickr.com/800/600/{clave}?lock={self.pk}'

    # Palabra del nombre (sin tildes) -> artículo de Wikipedia cuya foto representa el producto
    WIKI = [
        ('mouse pad', 'Mousepad'), ('mouse', 'Computer mouse'), ('laptop', 'Laptop'), ('teclado', 'Computer keyboard'),
        ('audifono', 'Headphones'), ('parlante', 'Loudspeaker'), ('smartwatch', 'Smartwatch'),
        ('tablet', 'Tablet computer'), ('monitor', 'Computer monitor'), ('webcam', 'Webcam'),
        ('ssd', 'Solid-state drive'), ('usb', 'USB flash drive'), ('cargador', 'Battery charger'),
        ('power bank', 'Power bank'), ('router', 'Router (computing)'), ('smartphone', 'Smartphone'),
        ('microfono', 'Microphone'), ('impresora', 'Printer (computing)'), ('camara', 'Closed-circuit television'),
        ('lampara', 'Lamp'), ('sabana', 'Bed sheet'), ('licuadora', 'Blender'), ('cafetera', 'Drip coffee maker'),
        ('freidora', 'Air fryer'), ('olla', 'Cookware and bakeware'), ('almohada', 'Pillow'),
        ('aspiradora', 'Robotic vacuum cleaner'), ('ventilador', 'Mechanical fan'), ('toalla', 'Towel'),
        ('silla', 'Office chair'), ('escritorio', 'Desk'), ('organizador', 'Desk'), ('soporte', 'Laptop'),
        ('pizarra', 'Whiteboard'), ('calculadora', 'Scientific calculator'), ('resaltador', 'Highlighter'),
        ('archivador', 'Filing cabinet'), ('mochila', 'Backpack'), ('cuaderno', 'Notebook'),
        ('zapatilla', 'Sneakers'), ('bicicleta', 'Mountain bike'), ('colchoneta', 'Yoga'),
        ('casco', 'Bicycle helmet'), ('polera', 'T-shirt'), ('basquet', 'Basketball'),
        ('cuerda', 'Jump rope'), ('botella', 'Water bottle'), ('pelota', 'Football (ball)'),
        ('mancuerna', 'Dumbbell'),
    ]

    @property
    def wiki_titulo(self):
        nombre = ''.join(c for c in unicodedata.normalize('NFD', self.nombre.lower())
                         if unicodedata.category(c) != 'Mn')
        return next((t for palabra, t in self.WIKI if palabra in nombre), '')
