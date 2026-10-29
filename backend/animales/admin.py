from django.contrib import admin
from .models import Animal, Evento, SolicitudAdopcion

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'estado', 'fecha_nacimiento')
    list_filter = ('especie', 'estado')
    search_fields = ('nombre',)

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nombre_animal', 'especie', 'fecha', 'gestionada')
    list_filter = ('gestionada', 'especie')
    search_fields = ('nombre', 'email', 'nombre_animal')
    readonly_fields = ('animal', 'nombre_animal', 'especie', 'nombre', 'email', 'telefono', 'respuestas', 'fecha')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'lugar')
    search_fields = ('titulo', 'lugar')
