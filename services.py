from django.core.exceptions import ObjectDoesNotExist
from .models import Inmueble, User, ContactForm
from .baseModel import BaseModel

# crear un objeto con el modelo
def create_inmueble(data):
    try:
        inmueble = Inmueble.objects.create(**data)
        inmueble.save()
        return inmueble
    except Exception as e:
        return str(e)

# enlistar desde el modelo de datos
def list_inmuebles():
    try:
        inmuebles = Inmueble.objects.all()
        return inmuebles
    except Exception as e:
        return str(e)

# actualizar un registro en el modelo de datos
def update_inmueble(inmueble_id, data):
    try:
        inmueble = Inmueble.objects.get(id=inmueble_id)
        for key, value in data.items():
            setattr(inmueble, key, value)
        inmueble.save()
        return inmueble
    except ObjectDoesNotExist:
        return "Inmueble not found."
    except Exception as e:
        return str(e)

# borrar un registro del modelo de datos utilizando un modelo Django
def delete_inmueble(inmueble_id):
    try:
        inmueble = Inmueble.objects.get(id=inmueble_id)
        inmueble.delete()
        return "Inmueble deleted successfully."
    except ObjectDoesNotExist:
        return "Inmueble not found."
    except Exception as e:
        return str(e)
    
#funcion que guarda un listado de inmuebles de cierto nombre 
def get_inmuebles(nombre, descripcion):
    inmuebles = Inmueble.objects.filter(nombre__contains=nombre)
    if descripcion is not None:
        inmuebles = inmuebles.filter(descripcion__contains=descripcion)

    archivo =open('propiedades_nombre_desc.txt', 'w')

    for inmu in inmuebles:
        archivo.write(inmu.nombre+' - '+inmu.descripcion+'\n')
    archivo.close()

#funcion que, usando SQL, busca las propiedades listadas por comuna   
def get_raw_inmuebles(comuna_nombre):
    query = """
            select inmu.id, inmu.nombre, inmu.descripcion, comu.nombre as comuna, reg.nombre as region    
            from core_inmueble inmu
            inner join core_comuna comu
            ON inmu.comuna_id = comu.id
            inner join core_region reg
            ON inmu.region_id = reg.id
            where comu.nombre like '%"""+ str(comuna_nombre)+ """%' """
            #where comu.id = 1
    
    inmuebles = Inmueble.objects.raw(query)

    archivo =open('propiedades_x_comuna.txt', 'w')

    for inmu in inmuebles:

        archivo.write(inmu.nombre+' - '+inmu.descripcion+'\n')
    
    archivo.close()