from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

# Lado máximo en píxeles: suficiente para verse bien en pantalla grande sin pesar varios MB
LADO_MAXIMO = 1600


def optimizar_imagen(archivo):
    """Endereza las fotos del móvil (EXIF), las reduce y las guarda como JPEG."""
    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)
    imagen.thumbnail((LADO_MAXIMO, LADO_MAXIMO))
    if imagen.mode != 'RGB':
        imagen = imagen.convert('RGB')

    salida = BytesIO()
    imagen.save(salida, format='JPEG', quality=85, optimize=True)
    nombre = Path(archivo.name).stem + '.jpg'
    return ContentFile(salida.getvalue(), name=nombre)
