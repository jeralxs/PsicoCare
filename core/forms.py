from django import forms
from django.forms import ModelForm, fields, Form, ModelMultipleChoiceField
from .models import Test, Psicologo, Usuario, Generopsicologo, Tiposesion, Corrientepsicologica, Rangoetario, Rangoprecio, Motivosesion, Coberturasalud, Diagnostico, Resena
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox



form_hidden = {'class': 'd-none'}
form_select = {'class': 'form-select'}
form_control = {'class': 'form-control'}
form_text_area = {'class': 'form-control', 'rows': '1'}
form_file = {'class': 'form-control-file', 'title': 'Debe subir una imagen'}
form_check = {'class': 'form-check-input'}
form_password = {'class': 'form-control text-danger'}

GENERO = (("1","Mujer"),("2","Hombre"),("3","Otro"))
class FormRegistro (UserCreationForm): 
    # username = forms.CharField(
    #     max_length=100, 
    #     required=True, 
    #     label='nombre de usuario',
    #     widget=forms.TextInput(attrs={'placeholder': 'Ingresa Usuario'}),
    # )
    # first_name = forms.CharField(
    #     max_length=100, 
    #     required=True, 
    #     label='nombres',
    #     widget=forms.TextInput(attrs={'placeholder': 'Ingresa nombres'}),
    # )

    # last_name = forms.CharField(
    #     max_length=100, 
    #     required=True, 
    #     label='apellido paterno',
    #     widget=forms.TextInput(attrs={'placeholder': 'Ingresa apellido paterno'}),
    # )

    apellido_materno = forms.CharField(
        max_length=100, 
        required=True, 
        label='apellido materno',
        widget=forms.TextInput(attrs={'placeholder': ''}),
    )

    genero_idgenero = forms.MultipleChoiceField(
        required=True, 
        label='Género',
        widget=forms.Select,
        choices=GENERO,
    )

    # email = forms.EmailField(
    #     required=True,
    #     label='correo',
    #     widget=forms.EmailInput(attrs={'placeholder': 'Ingresa correo'})
    # )

    password = forms.CharField(
        max_length=20, 
        required=True, 
        label='contraseña',
        widget=forms.PasswordInput (attrs={'placeholder': ''}),
    )

    password2= forms.CharField(
        label='confirmar contraseña',
        widget=forms.PasswordInput (attrs={'placeholder': ''}),
    )

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'apellido_materno', 'email', 'genero_idgenero', 'password', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(form_control)
        self.fields['first_name'].widget.attrs.update(form_control)
        self.fields['last_name'].widget.attrs.update(form_control)
        self.fields['email'].widget.attrs.update(form_control)
        self.fields['password'].widget.attrs.update(form_control)
        self.fields['password2'].widget.attrs.update(form_control)




GENERO = (("1","Mujer"),("2","Hombre"),("3","Otro"))
class FormRegistroPsi (UserCreationForm): 
    # username = forms.CharField(
    #     max_length=100, 
    #     required=True, 
    #     label='nombre de usuario',
    #     widget=forms.TextInput(attrs={'placeholder': 'Ingresa Usuario'}),
    # )
    # first_name = forms.CharField(
    #     max_length=100, 
    #     required=True, 
    #     label='nombres',
    #     widget=forms.TextInput(attrs={'placeholder': 'Ingresa nombres'}),
    # )

    # last_name = forms.CharField(
    #     max_length=100, 
    #     required=True, 
    #     label='apellido paterno',
    #     widget=forms.TextInput(attrs={'placeholder': 'Ingresa apellido paterno'}),
    # )

    apellido_materno = forms.CharField(
        max_length=100, 
        required=True, 
        label='apellido materno',
        widget=forms.TextInput(attrs={'placeholder': ''}),
    )

    genero_idgenero = forms.MultipleChoiceField(
        required=True, 
        label='Género',
        widget=forms.Select,
        choices=GENERO,
    )

    # email = forms.EmailField(
    #     required=True,
    #     label='correo',
    #     widget=forms.EmailInput(attrs={'placeholder': 'Ingresa correo'})
    # )

    password = forms.CharField(
        max_length=20, 
        required=True, 
        label='contraseña',
        widget=forms.PasswordInput (attrs={'placeholder': ''}),
    )

    password2= forms.CharField(
        label='confirmar contraseña',
        widget=forms.PasswordInput (attrs={'placeholder': ''}),
    )

    licencia= forms.CharField(
        label='Número de registro de licencia',
        widget=forms.TextInput(attrs={'placeholder': ''}),
    )

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'apellido_materno', 'genero_idgenero', 'email', 'password', 'password2', 'licencia']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(form_control)
        self.fields['first_name'].widget.attrs.update(form_control)
        self.fields['last_name'].widget.attrs.update(form_control)
        self.fields['email'].widget.attrs.update(form_control)
        self.fields['password'].widget.attrs.update(form_control)
        self.fields['password2'].widget.attrs.update(form_control)

class IngresarForm(Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingresar Usuario'}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'}), label="Contraseña")
    class Meta:
        model = Usuario
        fields = ['username', 'password']

class PasswordResetForm(Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingresar correo'}), label="Correo")
    class Meta:
        model = Usuario
        fields = ['email']

# FORMS PERFIL

class DatosPersonalesForm (forms.ModelForm): 
    edit_per = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = forms.CharField(
        max_length=100, 
        required=True, 
        label='nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa nombre de usuario'}),
    )

    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        label='nombres',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa nombres'}),
    )

    last_name = forms.CharField(
        max_length=100, 
        required=True, 
        label='apellido paterno',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa apellido paterno'}),
    )

    apellido_materno = forms.CharField(
        max_length=100, 
        required=True, 
        label='apellido materno',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa apellido materno'}),
    )

    email = forms.EmailField(
        required=True,
        label='correo',
        widget=forms.EmailInput(attrs={'placeholder': 'Ingresa correo'})
    )

    password = forms.CharField(
        max_length=20, 
        required=True, 
        label='contraseña',
        widget=forms.PasswordInput (attrs={'placeholder': 'Ingresa contraseña'}),
    )
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'apellido_materno', 'email', 'password']



EDAD_OP = (("1","Infanto-juvenil"),("2","Adultos"),("3","Adulto mayor"))
PCORRIENTE_OP=(("1","Cognitivo-Conductual"),("2","Psicoanálisis"),("3","Sistémica"),("4","Humanista"),("5","Breve"),("6","Feminista"))
PRECIO_OP=(("1","$0-$10000"),("2","$10000-$15000"),("3","$15000-$20000"),("4","$25000-$30000"),("5","$30000-$35000"),("6","$35000-$40000"),
                ("7","$40000-$45000"),("8","$45000-$50000"),("9","+$50000"))
COBERTURA_OP=(("1","Fonasa"),("2","Isapre"),("3","Otro"),("4","Ninguno"))

class DatosProfesionalesForm (forms.ModelForm): 
    edit_prof = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rango_etario = forms.MultipleChoiceField(
        required=True, 
        label='Rango etario',
        widget=forms.Select,
        choices=EDAD_OP,
    )

    corriente_psicologica = forms.MultipleChoiceField(
        required=True, 
        widget=forms.Select,
        choices=PCORRIENTE_OP,
    )

    esp_diagnostica = forms.CharField(
        max_length=100, 
        required=True, 
        label='Especialidad diagnóstica',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese especialidad diagnóstica'}),
    )

    areas_trabajo = forms.CharField(
        max_length=100, 
        required=True, 
        label='Áreas de trabajo',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa áreas con las que trabaja'}),
    )

    rango_precio = forms.MultipleChoiceField(
        required=True, 
        label='Rango de precio',
        widget=forms.Select,
        choices=PRECIO_OP,
    )

    cobertura_aceptada = forms.MultipleChoiceField(
        required=True, 
        label='Cobertura de salud que acepta',
        widget=forms.Select,
        choices=COBERTURA_OP,
    )
    numeroregistrolicencia  = forms.CharField(
        max_length=100, 
        required=True, 
        label='Número registro de licencia',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa número registro licencia'}),
    )

    class Meta:
        model = Psicologo
        fields = ['rango_etario','corriente_psicologica','esp_diagnostica','areas_trabajo','rango_precio','cobertura_aceptada','numeroregistrolicencia']

class EliminarForm(Form):
    eliminar_cuenta = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'}), label="Contraseña")
    
    class Meta:
        model = Usuario
        fields = ['password']

# FORMS PERFIL
from django import forms
from .models import Mensaje

class FormularioMensaje(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']  # Asumiendo que el campo se llama 'contenido' en tu modelo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].widget.attrs.update({
            'rows': 3, 
            'placeholder': 'Escribe tu mensaje aquí',
            'class': 'form-control'
        })
        self.fields['contenido'].label = ''  # Quita la etiqueta del campo

class ConversationForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=None,
        empty_label="Selecciona un destinatario",
        label="Iniciar conversación con"
    )

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        
        if user_type == 'psicologo':
            from .models import Paciente
            self.fields['recipient'].queryset = Paciente.objects.all()
        elif user_type == 'paciente':
            from .models import Psicologo
            self.fields['recipient'].queryset = Psicologo.objects.all()

# form test psico

class FormTestPaciente(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        exclude = ['idtest','idusuariotest']
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id
    
    generopsicologo_idgenero = forms.ModelChoiceField(
        
        queryset=Generopsicologo.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Preferencia de género',
        
    )
    rangoetario_idrangoetario = forms.ModelChoiceField(
        queryset=Rangoetario.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Rango de edad'
    )
    tiposesion_idtiposesion = forms.ModelChoiceField(
        queryset=Tiposesion.objects.all(),
    
        widget=forms.Select(attrs=form_select),
        label='Tipo de sesión'
    )
    corriente_idcorriente = forms.ModelChoiceField(
        queryset=Corrientepsicologica.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Preferencia de de corriente psicológica'
    )
    diagnostico_iddiagnostico = forms.ModelChoiceField(
        queryset=Diagnostico.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Diagnósticos o sospechas'
    )
    motivosesion_idmotivosesion = forms.ModelChoiceField(
        queryset=Motivosesion.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Motivo por el que busca ayuda'
    )
    rangoprecio_idrangoprecio = forms.ModelChoiceField(
        queryset=Rangoprecio.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Rango de precio que puede pagar'
    )
    coberturasalud_idcobertura = forms.ModelChoiceField(
        queryset=Coberturasalud.objects.all(),
        widget=forms.Select(attrs=form_select),
        label='Cobertura de salud'
    )

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['puntuacion', 'comentarios']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} estrellas') for i in range(1, 6)])
        }
