from django.contrib import admin
from .models import Animal, Evento

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'fecha_nacimiento')
    list_filter = ('estado',)
    search_fields = ('nombre',)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'lugar')
    search_fields = ('titulo', 'lugar')
