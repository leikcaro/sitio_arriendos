from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Inmueble, Cliente, Region, Comuna

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_terreno', 'cantidad_estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'direccion', 'comuna', 'tipo_inmueble']

class ContactFormForm(forms.Form):
    customer_email = forms.EmailField(label='email' )
    customer_name = forms.CharField(max_length=64, label='name' )
    message = forms.CharField(label='message' )
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=64, 
        label="Nombre", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
class UserFormForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# class UserRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Cliente
#         fields = ['rut', 'name', 'lastname', 'email', 'phone', 'adress']
#         widgets = {
#             'RUT': forms.TextInput(attrs={'class': 'form-control'}),
#             'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
#             'Apellidos': forms.TextInput(attrs={'class': 'form-control'}),
#             'E-Mail': forms.EmailInput(attrs={'class': 'form-control'}),
#             'Teléfono': forms.TextInput(attrs={'class': 'form-control'}),
#             'Dirección': forms.TextInput(attrs={'class': 'form-control'}),
#             #'tipo_usuario': forms.CheckboxInput(attrs={'class': 'form-check'}),
#         }

class RegistroForm(UserCreationForm):
    #estos son los atributos "extra" que son de Cliente, van acá por orden pero se usa en principio User y sus 3 valores base, posteriormente se usa los de Cliente.
    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    adress = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta: # Define el modelo y los campos que deben estar presentes en el formulario
        model = User
        fields = ['username', 'password1', 'password2'] # van solo los de User

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        #form-control da las propiedades de Bootstrap
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
    def save(self, commit=True):
        #se guardan los campos de user para crear un nuevo User
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            cliente = Cliente(
                user=user,
                rut=self.cleaned_data['rut'],
                name=self.cleaned_data['name'],
                lastname=self.cleaned_data['lastname'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                adress=self.cleaned_data['adress'],
                tipo_usuario_id=1  # Asigna el valor por defecto para 'arrendatario'
            )
            cliente.save()
        return user
    
# Form para la modificacion de los datos del cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['name', 'lastname', 'email', 'phone', 'adress', 'tipo_usuario']  # Excluir 'rut'
        

class FiltroRegionComunaForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), required=False, label="Comuna")

    def __init__(self, *args, **kwargs):
        super(FiltroRegionComunaForm, self).__init__(*args, **kwargs)
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['comuna'].queryset = Comuna.objects.none()
        else:
            self.fields['comuna'].queryset = Comuna.objects.none()