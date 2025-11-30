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