from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Inmueble, Cliente, Tipo_inmueble, Comuna, Region
from core.models import ContactForm
from .forms import ContactFormForm, LoginForm, UserFormForm, RegistroForm, InmuebleForm, FiltroRegionComunaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib.auth.models import Group
#from django_ratelimit.decorators import ratelimit
import logging  
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ClienteForm
from django.http import JsonResponse
#from django.http import HttpResponseRedirect

# from .forms import ContactFormModelForm
# from .forms import CustomUserCreationForm
# from django.contrib.auth import authenticate
#from .models import ContactForm


# Create your views here.

def home(request):
    form = FiltroRegionComunaForm(request.GET or None)
    inmuebles = Inmueble.objects.all()

    if request.GET and form.is_valid():
        if form.cleaned_data['comuna']:
            inmuebles = inmuebles.filter(comuna=form.cleaned_data['comuna'])
        elif form.cleaned_data['region']:
            inmuebles = inmuebles.filter(comuna__region=form.cleaned_data['region'])

    return render(request, 'home.html', {'form': form, 'inmuebles': inmuebles})

def about(request):
    return render(request, 'about.html', {})

@login_required
def welcome(request):

    return render(request, 'welcome.html', {}) 

def contact(request):
    #validar metodo post
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        #validar información correcta
        if form.is_valid():
            #guardado de la información en la base de datos
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            # redirección del metodo
            #return HttpResponseRedirect('/success')
            return redirect('/success')

    else: 
        # redirección del metodo
        form = ContactFormForm()
    return render(request,'contact.html',{'form':form})

def success(request):
    return render(request, 'success.html') 

def success(request):
    return render(request, 'success.html') 

logger = logging.getLogger(__name__)

#@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def login_view(request):
    was_limited = getattr(request, 'limited', False)
    
    # Registro si la tasa límite fue excedida
    if was_limited:
        logger.warning('Rate limit exceeded for IP: %s', request.META['REMOTE_ADDR'])
        return HttpResponse('Rate limit exceeded', status=429)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        logger.debug('Processing POST request with login form.')

        if form.is_valid():
            logger.debug('Form is valid.')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                logger.info('Authentication successful, redirecting to welcome.')
                return redirect('welcome')
            else:
                logger.warning('Authentication failed.')
                form.add_error(None, 'Credenciales inválidas')
        else:
            logger.warning('Form is invalid: %s', form.errors)

    else:
        logger.debug('Rendering form for GET request.')
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'error': form.non_field_errors()})

def logged_out(request):
    return render(request, 'logged_out.html')

def ratelimit_exceeded(request, exception):
    return HttpResponse('Rate limit exceeded. Please try again later.', status=429)

#@ratelimit(key='ip', rate='3/m', block=True)
# def test_ratelimit(request):
#     if getattr(request, 'limited', False):
#         return HttpResponse('Rate limit exceeded', status=429)
#     return HttpResponse('Rate limit not exceeded')

def ratelimit_exceeded(request, exception):
    return HttpResponse('Ha superado el numero de intentos de login, ingrese al sitio más tarde.', status=429)

def logged_out(request):
    return render(request, 'logged_out.html') 


def registration_view(request):
    if request.method == 'POST':
        form = UserFormForm(request.POST)
        if form.is_valid():
            User.objects.create(**form.cleaned_data)
            return redirect('welcome')  # Redirige a la página de bienvenida
    else:
        form = UserFormForm()
    return render(request, 'registration_form.html', {'form': form})


######################editar el perfil########################
@login_required
def mi_perfil(request):
    cliente = Cliente.objects.get(user=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a una página de perfil después de guardar los cambios
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'mi_perfil.html', {'form': form, 'cliente': cliente})

def add_group_client(request, cliente_id):
    client = User.objects.get(pk="name")
    group = Group.objects.get(name="Cliente")
    
    # Agregar el cliente al grupo
    client.groups.add(group)
    
    return HttpResponse("Cliente agregado al grupo exitosamente")

def contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            ContactForm.objects.create(**form.cleaned_data)
            return redirect('success')
    else:
        form = ContactFormForm()
    return render(request, 'contact.html', {'form': form})

def success(request):
    return render(request, 'success.html')

# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')  # Redirige a la página de inicio después del registro
    # else:
    #     form = UserRegistrationForm()
    # return render(request, 'registration/register.html', {'form': form})

@login_required
def listar_propiedades(request):
    #cliente = get_object_or_404(Cliente, user=request.user)
    propiedades = Inmueble.objects.filter(arrendador=request.user)
    
    return render(request, 'listar_propiedades.html', {'propiedades': propiedades})

@login_required
def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.cliente = get_object_or_404(User, user=request.user)
            inmueble.save()
            return redirect('listar_propiedades')
    else:
        form = InmuebleForm()
    return render(request, 'agregar_inmueble.html', {'form': form})

def comuna(request):
    context={
        #'tipo_usuario': request.user.cliente.tipo_usuario.nombre,
        'tipo_inmuebles': Tipo_inmueble.objects.all()
        
    }
    print(Tipo_inmueble.objects.all())
    # if request.method == 'POST':
    #     form = ComunaForm(request.POST)
    #     if form.is_valid():
            
            
    #         return redirect('listar_propiedades')
    # else:
    #     form = InmuebleForm()
    return render(request, 'comuna.html', context) 

class InmueblesListView(ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = Inmueble
    template_name =''
    paginate_by = 10

    def get_queryset(self):
        return 

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('nombre_de_la_vista_a_redirigir')  # Redirige a donde desees
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def cargar_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

# def register(request):
#     if request.method == 'POST':
#         username=request.POST["username"]
#         email=request.POST["email"]
#         password=request.POST["password"]
#         rut=request.POST["rut"]
#         nombre=request.POST["nombre"]
#         apellido=request.POST["apellido"]
#         direccion=request.POST["direccion"]
#         telefono=request.POST["telefono"]
        
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})
# def ratelimit_exceeded(request, exception):
#     return HttpResponse('Rate limit exceeded. Please try again later.', status=429)

# @ratelimit(key='ip', rate='3/m', block=True)
# def test_ratelimit(request):
#     if getattr(request, 'limited', False):
#         return HttpResponse('Rate limit exceeded', status=429)
#     return HttpResponse('Rate limit not exceeded')

# def ratelimit_exceeded(request, exception):
#     return HttpResponse('Ha superado el numero de intentos de login, ingrese al sitio más tarde.', status=429)
