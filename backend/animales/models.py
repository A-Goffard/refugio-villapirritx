from django.db import models

class Animal(models.Model):
    ESTADOS = [
        ('ADOPCION', 'En Adopción'),
        ('ACOGIDA', 'Casa de Acogida'),
        ('ADOPTADO', 'Adoptado'),
        ('URGENTE', 'Urgente'),
    ]
    # Decide qué cuestionario de adopción se pide (ver cuestionario.py)
    ESPECIES = [
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
    ]

    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=10, choices=ESPECIES, default='PERRO')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    descripcion = models.TextField(verbose_name="Descripción e Historia")
    foto = models.ImageField(upload_to='animales/', null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ADOPCION')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Solicitud(models.Model):
    TIPOS = [
        ('ACOGIDA', 'Casa de Acogida'),
        ('ADOPCION', 'Adopción'),
        ('VOLUNTARIADO', 'Voluntariado'),
        ('DONACION', 'Donación Material'),
        ('VIAJE', 'Viaje Solidario'),
        ('OTRO', 'Otro'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    mensaje = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Campo para marcar si ya se ha gestionado (útil para el panel)
    gestionada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"
    
    class Meta:
        verbose_name_plural = "Solicitudes y Contacto"

class SolicitudAdopcion(models.Model):
    """Cuestionario pre-adopción rellenado desde la web."""
    # Si se borra el animal, la solicitud se conserva (guardamos también su nombre)
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='solicitudes_adopcion')
    nombre_animal = models.CharField(max_length=50)
    especie = models.CharField(max_length=10, choices=Animal.ESPECIES)

    # Copiados de las respuestas para poder listar y buscar sin abrir el JSON
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    telefono = models.CharField(max_length=50)

    # {clave_pregunta: respuesta}, con las claves de cuestionario.py
    respuestas = models.JSONField(default=dict)
    fecha = models.DateTimeField(auto_now_add=True)
    gestionada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} → {self.nombre_animal}"

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Solicitud de adopción"
        verbose_name_plural = "Solicitudes de adopción"


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateField()
    horario = models.CharField(max_length=100, help_text="Ej: De 11:00 a 14:00")
    lugar = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=600, verbose_name="Descripción breve")
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"

    class Meta:
        ordering = ['fecha']
