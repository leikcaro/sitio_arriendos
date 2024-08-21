from django.contrib import admin
from .models import User, ContactForm, Inmueble, Cliente, Comuna, Region, Tipo_inmueble, Tipo_usuario
# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'name', 'lastname', 'email', 'phone', 'adress', 'created_at', 'updated_at')
    search_fields = ('email','rut')
    readonly_fields = ('created_at', 'updated_at')
    
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'message', 'created_at', 'updated_at')
    
@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 
        'descripcion', 
        'm2_construidos', 
        'm2_terreno', 
        'cantidad_estacionamientos', 
        'cantidad_habitaciones', 
        'cantidad_banos', 
        'direccion', 
        'comuna', 
        'tipo_inmueble',
        'arrendada',
        'foto_portada'
    )
    
@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')
    
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero')
    
@admin.register(Tipo_usuario)
class Tipo_usuarioAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')
    
@admin.register(Tipo_inmueble)
class Tipo_inmuebleAdmin(admin.ModelAdmin):
    list_display = ('id','nombre')