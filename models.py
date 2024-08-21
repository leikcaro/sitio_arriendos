from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
import uuid
from django.contrib.auth.models import User #se puede usar para unir usuario con user

# Create your models here.

class Region(models.Model):
    nombre=models.CharField(max_length=30)
    numero=models.IntegerField()
    def __str__(self):
        return f"{self.nombre}"
    
class Comuna(models.Model):
    nombre=models.CharField(max_length=30)
    region=models.ForeignKey(Region, max_length=30, on_delete=models.CASCADE, null=False)
    def __str__(self):
        return f"{self.nombre}"

class Tipo_usuario(models.Model):
    nombre=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.nombre}"
    
class Tipo_inmueble(models.Model):
    nombre=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.nombre}"
    
class Cliente(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE, null= False)
    rut= models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=30, null=False, blank=False)
    lastname = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False) 
    phone= models.CharField(max_length=30, null=False, blank=False)
    adress = models.CharField(max_length=50, null=False, blank=False)
    tipo_usuario=models.ForeignKey(Tipo_usuario,on_delete=models.CASCADE, default="arrendador") #agrega el _id automaticamente la BBDD
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} {self.lastname}"
    
class Inmueble(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    m2_construidos = models.FloatField(null=False)
    m2_terreno = models.FloatField(null=False)
    cantidad_estacionamientos = models.IntegerField(default=0)
    cantidad_habitaciones = models.IntegerField(null=False)
    cantidad_banos = models.IntegerField(null=False)
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=False)
    tipo_inmueble = models.ForeignKey(Tipo_inmueble, max_length=100, on_delete=models.CASCADE, null=False)
    arrendador = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True, default="1")
    arrendatario = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE, blank=True)
    arrendada = models.BooleanField(default=False) #podria ser con la funcion if(hasatr) en arrendatario en vez de este.
    foto_portada = models.ImageField(upload_to="inmuebles", default="inmuebles/casa1.jpg")
    

    def __str__(self):
        return self.nombre
    
class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False) 
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()
    #revisar en la base de datos porque no seran visibles en el panel admin
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.customer_email} - Mensaje: {self.message}"
    