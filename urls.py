from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import home, about, welcome, contact, success, logged_out, login_view, listar_propiedades, agregar_inmueble, comuna, mi_perfil, cargar_comunas




urlpatterns = [

    path('propiedades/', listar_propiedades, name='listar_propiedades'),
    path('propiedades/agregar/', agregar_inmueble, name='agregar_inmueble'),
    path('propiedades/comuna/', comuna, name='comuna'),
    path('mi_perfil/', mi_perfil, name='mi_perfil'),
    path('ajax/cargar-comunas/', cargar_comunas, name='cargar_comunas'),
]
    
