from django import forms
from django.forms import ModelForm, fields, Form
from .models import Test, Psicologo, Usuario
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


form_hidden = {'class': 'd-none'}
form_select = {'class': 'form-select'}
form_control = {'class': 'form-control'}
form_text_area = {'class': 'form-control', 'rows': '1'}
form_file = {'class': 'form-control-file', 'title': 'Debe subir una imagen'}
form_check = {'class': 'form-check-input'}
form_password = {'class': 'form-control text-danger'}

class FormRegistro (forms.ModelForm): 
    username = forms.CharField(
        max_length=100, 
        required=True, 
        label='nombre de usuario',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa Usuario'}),
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

    apellidomaterno = forms.CharField(
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

    password2= forms.CharField(
        label='confirmar contraseña',
        widget=forms.PasswordInput (attrs={'placeholder': 'Repita la contraseña'}),
    )

    licencia= forms.CharField(
        label='Número de registro de licencia',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa número de RNPI'}),
    )

    class Meta:
        model = Usuario
        fields = ['username','first_name', 'last_name', 'apellidomaterno', 'email', 'password', 'licencia']


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

# form test psico

GENERO_OP=(("1","Mujer"),("2","Hombre"),("3","Otro"),("4","Sin preferencia"))
TERAPIA_OP=(("1","Individual"),("2","Pareja"),("3","Familiar"))
CORRIENTE_OP=(("1","Cognitivo-Conductual"),("2","Psicoanálisis"),("3","Sistémica"),("4","Humanista"),("5","Breve"),("6","Feminista"),("7","Otra"),("8","Sin preferencia"))
DIAGNOSTICO_OP=(("1","Ansiedad"),("2","Autolesiones"),("3","Depresión"),("4","Riesgo suicida"),("5","Trastorno disociativo"),("6","Trastorno de estrés postraumático"),
                ("7","Crisis de pánico"),("8","Disfunciones sexuales"),("9","Bipolaridad"),("10","Consumo problemático"),("11","Trastorno conducta alimentaria"),
                ("12","Trastorno de la personalidad"),("13","Trastorno obsesivo compulsivo"),("14","Trastorno psicótico"),("15","Otro"),("16","Sin diagnóstico o sospecha"))
MOTIVO_OP=(("1","Acoso"),("2","Bullying"),("3","Crisis existencial"),("4","Duelo"),("5","Estrés"),("6","Problemas vocacionales"),
                ("7","Problemas de relaciones"),("8","Problemas de autoestima"),("9","Sexualidad y/o género"),("10","Otro"))
PRECIO_OP=(("1","$0-$10000"),("2","$10000-$15000"),("3","$15000-$20000"),("4","$25000-$30000"),("5","$30000-$35000"),("6","$35000-$40000"),
                ("7","$40000-$45000"),("8","$45000-$50000"),("9","+$50000"))
COBERTURA_OP=(("1","Fonasa"),("2","Isapre"),("3","Otro"),("4","Ninguno"))

class FormTestPaciente (forms.ModelForm): 

    class Meta:
        model = Test
        fields = ['generopsicologo_idgeneropsicologo','tiposesion_idtiposesion','corrientepsicologica_idcorrientepsicologica','diagnostico_iddiagnostico','motivosesion_idmotivosesion','rangoprecio_idrangoprecio','coberturasalud_idcoberturasalud']

    pref_genero = forms.MultipleChoiceField(
        required=True, 
        widget=forms.Select.allow_multiple_selected,
        choices=GENERO_OP,
    )

    tipo_terapia = forms.MultipleChoiceField(
        required=True, 
        widget=forms.Select.allow_multiple_selected,
        choices=TERAPIA_OP,
    )

    pref_corriente = forms.MultipleChoiceField(
        required=True, 
        widget=forms.CheckboxSelectMultiple,
        choices=CORRIENTE_OP,
    )

    diagnostico_sospecha = forms.MultipleChoiceField(
        required=True, 
        widget=forms.CheckboxSelectMultiple,
        choices=DIAGNOSTICO_OP,
    )

    motivo_busqueda = forms.MultipleChoiceField(
        required=True, 
        widget=forms.CheckboxSelectMultiple,
        choices=MOTIVO_OP,
    )

    rango_precio = forms.MultipleChoiceField(
        required=True, 
        widget=forms.Select.allow_multiple_selected,
        choices=PRECIO_OP,
    )

    cobertura_salud = forms.MultipleChoiceField(
        required=True, 
        widget=forms.Select.allow_multiple_selected,
        choices=COBERTURA_OP,
    )