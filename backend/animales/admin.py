from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'fecha_nacimiento')
    list_filter = ('estado',)
    search_fields = ('nombre',)