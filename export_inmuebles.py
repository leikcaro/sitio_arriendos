import os
import sys
import django

# Asegurarte de que el directorio del proyecto está en sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''Explocacion de como se llega a estesys.path
__file__: __file__ es una variable especial en Python que contiene la ruta del archivo actual. En este caso, será la ruta completa al archivo export_inmuebles.py.
os.path.abspath(__file__): os.path.abspath(__file__) convierte la ruta relativa de __file__ a una ruta absoluta. Esto asegura que tenemos la ruta completa al archivo export_inmuebles.py.
os.path.dirname(os.path.abspath(__file__)): os.path.dirname(path) devuelve el directorio que contiene el archivo especificado por path. En este caso, os.path.dirname(os.path.abspath(__file__)) devuelve el directorio que contiene export_inmuebles.py, que es core.
os.path.dirname(os.path.dirname(os.path.abspath(__file__))): Llamamos a os.path.dirname una segunda vez para subir un nivel más en la jerarquía de directorios. Esto devuelve el directorio padre del directorio core, que es el directorio principal del proyecto sitio_arriendos.'''

print(sys.path)  # Añade esta línea para imprimir sys.path

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sitio_arriendos.settings')
django.setup()

from core.models import Inmueble, Comuna, Region

# Función para exportar inmuebles
def export_inmuebles_comuna():
    inmuebles_por_comuna = {}

    # Obtener todas las comunas
    comunas = Comuna.objects.all()

    for comuna in comunas:
        # Obtener inmuebles en la comuna actual
        inmuebles = Inmueble.objects.filter(comuna=comuna, arrendada=False).values('nombre', 'descripcion')

        # Agregar los inmuebles al diccionario
        inmuebles_por_comuna[comuna.nombre] = list(inmuebles)

    # Guardar los resultados en un archivo de texto
    with open('inmuebles_para_arriendo.txt', 'w', encoding='utf-8') as file:
        for comuna, inmuebles in inmuebles_por_comuna.items():
            file.write(f'Comuna: {comuna}\n')
            for inmueble in inmuebles:
                file.write(f"Nombre: {inmueble['nombre']}\n")
                file.write(f"Descripción: {inmueble['descripcion']}\n")
                file.write('\n')
            file.write('\n')
            
# Función para exportar inmuebles por región
def export_inmuebles_region():
    inmuebles_por_region = {}

    # Obtener todas las regiones
    regiones = Region.objects.all()

    for region in regiones:
        # Obtener inmuebles en la región actual
        inmuebles = Inmueble.objects.filter(comuna__region=region, arrendada=False).values('nombre', 'descripcion')

        # Agregar los inmuebles al diccionario
        inmuebles_por_region[region.nombre] = list(inmuebles)

    # Guardar los resultados en un archivo de texto
    with open('inmuebles_para_arriendo_reg.txt', 'w', encoding='utf-8') as file:
        for region, inmuebles in inmuebles_por_region.items():
            file.write(f'Region: {region}\n')
            for inmueble in inmuebles:
                file.write(f"Nombre: {inmueble['nombre']}\n")
                file.write(f"Descripción: {inmueble['descripcion']}\n")
                file.write('\n')
            file.write('\n')

# Si se ejecuta este script, se puede elegir que se ejecute la función de exportación por comuna o región, comentando la no deseada
if __name__ == '__main__':
    #export_inmuebles_comuna()
    export_inmuebles_region()





