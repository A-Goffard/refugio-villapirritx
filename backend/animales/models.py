from django.db import models

class Animal(models.Model):
    ESTADOS = [
        ('ADOPCION', 'En Adopción'),
        ('ACOGIDA', 'Casa de Acogida'),
        ('ADOPTADO', 'Adoptado'),
        ('URGENTE', 'Urgente'),
    ]

    nombre = models.CharField(max_length=50)
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