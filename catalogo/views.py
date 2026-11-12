import unicodedata
from django.shortcuts import render
from django.views.generic import ListView
from .models import Producto
def normalizar(texto):
    """Minúsculas y sin tildes: 'Audífono' -> 'audifono'."""
    texto = unicodedata.normalize('NFD', texto.lower())
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
def terminos(consulta):
    """Divide la búsqueda en palabras y quita la 's' final (plural simple)."""
    return [t[:-1] if len(t) > 3 and t.endswith('s') else t
            for t in normalizar(consulta).split()]
def home(request):
    """Página de inicio: ejemplo de vista basada en función con contexto."""
    contexto = {
        'titulo': 'Bienvenido a la Tienda Django',
        'total_productos': Producto.objects.count(),
        'disponibles': Producto.objects.filter(disponible=True).count(),
    }
    return render(request, 'catalogo/home.html', contexto)
class ProductoListView(ListView):
    """Catálogo: ejemplo de vista basada en clase (ListView)."""
    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 12
    def get_queryset(self):
        qs = Producto.objects.all()
        categoria = self.request.GET.get('categoria')
        if categoria:
            qs = qs.filter(categoria=categoria)
        q = self.request.GET.get('q', '').strip()
        if q:
            palabras = terminos(q)
            ids = [
                p.pk for p in qs
                if all(w in normalizar(f'{p.nombre} {p.descripcion} {p.get_categoria_display()}')
                       for w in palabras)
            ]
            qs = qs.filter(pk__in=ids)
        return qs

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Catálogo de Productos'
        contexto['categorias'] = Producto.CATEGORIAS
        contexto['q'] = self.request.GET.get('q', '').strip()
        contexto['categoria_actual'] = self.request.GET.get('categoria', '')
        return contexto
