# Tienda Django – Guía Práctica Semana 11

**Asignatura:** Desarrollo de Aplicaciones Web (IS093A) – UNCP
**Autor:** Hinojosa Yaranga, Renzo Sebastián · GitHub: [RenzoHinojosa](https://github.com/RenzoHinojosa)
**Tema:** Introducción a Django: arquitectura MTV, URLs, vistas (FBV/CBV), plantillas y modelos (ORM)

## Qué incluye
| Capa MTV | Archivo | Contenido |
|---|---|---|
| Model | `catalogo/models.py` | Modelo `Producto` (ORM, `__str__`, propiedad `stock_bajo`) |
| Template | `templates/base.html`, `catalogo/templates/catalogo/*.html` | Herencia (`extends`), bloques, `for`, `if`, `url`, filtros (`title`, `date`, `floatformat`) |
| View | `catalogo/views.py` | 1 FBV (`home`) y 1 CBV (`ProductoListView`) |
| URLs | `config/urls.py`, `catalogo/urls.py` | `include()`, `path()` con `name` |

## Ejecución local
```bash
# 1. Entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

# 2. Dependencias
pip install -r requirements.txt

# 3. Base de datos
python manage.py check
python manage.py migrate

# 4. Datos de ejemplo
python manage.py poblar

# 5. administrador y pruebas
python manage.py createsuperuser
python manage.py test

# 6. Servidor
python manage.py runserver
```
Abrir: http://127.0.0.1:8000/ · http://127.0.0.1:8000/catalogo/ · http://127.0.0.1:8000/admin/

## Consultas ORM (shell)
```bash
python manage.py shell
```
```python
from catalogo.models import Producto
Producto.objects.all()
Producto.objects.filter(disponible=True)
Producto.objects.filter(categoria='tecnologia', precio__lt=200)
Producto.objects.exclude(stock=0).order_by('-precio')
Producto.objects.get(pk=1)
```
