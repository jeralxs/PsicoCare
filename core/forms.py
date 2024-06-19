from django import forms
from django.forms import ModelForm, fields, Form, ModelMultipleChoiceField
from .models import Test, Psicologo, Usuario, Generopsicologo, Tiposesion, Corrientepsicologica, Rangoetario, Rangoprecio, Motivosesion, Coberturasalud, Diagnostico
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm


form_hidden = {'class': 'd-none'}
form_select = {'class': 'form-select'}
form_control = {'class': 'form-control'}
form_text_area = {'class': 'form-control', 'rows': '1'}
form_file = {'class': 'form-control-file', 'title': 'Debe subir una imagen'}
form_check = {'class': 'form-check-input'}
form_password = {'class': 'form-control text-danger'}

GENERO = (("1","Mujer"),("2","Hombre"),("3","Otro"))
class FormRegistro (Form): 
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

    apellido_materno = forms.CharField(
        max_length=100, 
        required=True, 
        label='apellido materno',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa apellido materno'}),
    )

    genero_idgenero = forms.MultipleChoiceField(
        required=True, 
        label='Género',
        widget=forms.Select,
        choices=GENERO,
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

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Usuario
        fields = ['username','first_name', 'last_name', 'apellido_materno', 'email', 'password']




GENERO = (("1","Mujer"),("2","Hombre"),("3","Otro"))
class FormRegistroPsi (Form): 
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

    apellido_materno = forms.CharField(
        max_length=100, 
        required=True, 
        label='apellido materno',
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa apellido materno'}),
    )

    genero_idgenero = forms.MultipleChoiceField(
        required=True, 
        label='Género',
        widget=forms.Select,
        choices=GENERO,
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
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Usuario
        fields = ['username','first_name', 'last_name', 'apellido_materno', 'email', 'password', 'licencia']

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
        fields = ['content']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'rows': 3, 'placeholder': 'Escribe tu mensaje aquí'})

# form test psico

def get_genero():
    return [(g.idgeneropsicologo, g.genero) for g in Generopsicologo.objects.all()]
def get_tiposesion():
    return [(t.idtiposesion, t.nombre) for t in Tiposesion.objects.all()]
def get_corriente():
    return [(co.idcorrientepsicologica, co.corrientepsicologica) for co in Corrientepsicologica.objects.all()]
def get_diagnostico():
    return [(d.iddiagnostico, d.diagnostico) for d in Diagnostico.objects.all()]
def get_motivo():
    return [(m.idmotivosesion, m.motivosesion) for m in Motivosesion.objects.all()]
def get_precio():
    return [(r.idrangoprecio, f"{r.montominimo} - {r.montomaximo}") for r in Rangoprecio.objects.all()]
def get_cobertura():
    return [(cs.idcoberturasalud, cs.coberturasalud) for cs in Coberturasalud.objects.all()]

class FormTestPaciente(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        exclude = ['idtest','idusuariotest']
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['generopsicologo_idgeneropsicologo'].queryset = Generopsicologo.objects.all()
        self.fields['generopsicologo_idgeneropsicologo'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.idgeneropsicologo, str(obj.genero)) for obj in self.fields['generopsicologo_idgeneropsicologo'].queryset]
        )

        self.fields['tiposesion_idtiposesion'].queryset = Tiposesion.objects.all()
        self.fields['tiposesion_idtiposesion'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.idtiposesion, str(obj.nombre)) for obj in self.fields['tiposesion_idtiposesion'].queryset]
        )

        self.fields['corriente_idcorriente'].queryset = Corrientepsicologica.objects.all()
        self.fields['corriente_idcorriente'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.idcorrientepsicologica, str(obj.corrientepsicologica)) for obj in self.fields['corriente_idcorriente'].queryset]
        )

        self.fields['diagnostico_iddiagnostico'].queryset = Diagnostico.objects.all()
        self.fields['diagnostico_iddiagnostico'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.iddiagnostico, str(obj.diagnostico)) for obj in self.fields['diagnostico_iddiagnostico'].queryset]
        )

        self.fields['motivosesion_idmotivosesion'].queryset = Motivosesion.objects.all()
        self.fields['motivosesion_idmotivosesion'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.idmotivosesion, str(obj.motivosesion)) for obj in self.fields['motivosesion_idmotivosesion'].queryset]
        )

        self.fields['rangoprecio_idrangoprecio'].queryset = Rangoprecio.objects.all()
        self.fields['rangoprecio_idrangoprecio'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.idrangoprecio, f"{obj.montominimo} - {obj.montomaximo}") for obj in self.fields['rangoprecio_idrangoprecio'].queryset]
        )

        self.fields['coberturasalud_id'].queryset = Coberturasalud.objects.all()
        self.fields['coberturasalud_id'].widget = forms.CheckboxSelectMultiple(
            choices=[(obj.idcoberturasalud, str(obj.coberturasalud)) for obj in self.fields['coberturasalud_id'].queryset]
        )

    # def save(self, commit=True):
    #     instance = super().save(commit=False)

    #     if self.user:
    #         instance.idusuariotest = self.user.usuario 
    #         generopsicologo_ids = self.cleaned_data.get('generopsicologo_idgeneropsicologo', [])
    #         tiposesion_ids = self.cleaned_data.get('tiposesion_idtiposesion', [])
    #         corriente_ids = self.cleaned_data.get('corriente_idcorriente', [])
    #         diagnostico_ids = self.cleaned_data.get('diagnostico_iddiagnostico', [])
    #         motivosesion_ids = self.cleaned_data.get('motivosesion_idmotivosesion', [])
    #         rangoprecio_ids = self.cleaned_data.get('rangoprecio_idrangoprecio', [])
    #         coberturasalud_ids = self.cleaned_data.get('coberturasalud_id', [])
    #     if commit:
    #         instance.save()

    #         instance.generopsicologo_idgeneropsicologo.set(Generopsicologo.objects.filter(idgeneropsicologo__in=generopsicologo_ids))
    #         instance.tiposesion_idtiposesion.set(Tiposesion.objects.filter(idtiposesion__in=tiposesion_ids))
    #         instance.corriente_idcorriente.set(Corrientepsicologica.objects.filter(idcorrientepsicologica__in=corriente_ids))
    #         instance.diagnostico_iddiagnostico.set(Diagnostico.objects.filter(iddiagnostico__in=diagnostico_ids))
    #         instance.motivosesion_idmotivosesion.set(Motivosesion.objects.filter(idmotivosesion__in=motivosesion_ids))
    #         instance.rangoprecio_idrangoprecio.set(Rangoprecio.objects.filter(idrangoprecio__in=rangoprecio_ids))
    #         instance.coberturasalud_id.set(Coberturasalud.objects.filter(idcoberturasalud__in=coberturasalud_ids))

    #     return instance

#     class Meta:
#         model = Test
#         fields = '__all__'
#         exclude = ['idtest','idusuariotest']
# class FormTestPaciente(forms.ModelForm):
    
#     class Meta:
#                 model = Test
#                 fields = '__all__'
#                 exclude = ['idtest','idusuariotest'] 

#     generopsicologo_idgeneropsicologo = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_genero,
#     )

#     tiposesion_idtiposesion = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_tiposesion,
#     )

#     corriente_idcorriente = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_corriente,
#     )

#     diagnostico_iddiagnostico = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_diagnostico,
#     )

#     motivosesion_idmotivosesion = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_motivo,
#     )

#     rangoprecio_idrangoprecio = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_precio,
#     )

#     coberturasalud_id = forms.MultipleChoiceField(
#         required=True,
#         widget=forms.CheckboxSelectMultiple,
#         choices=get_cobertura,
#     )
#     def save(self, commit=True):
    
#         instance = super(FormTestPaciente, self).save(commit=False)
       
#         generopsicologo_ids = self.cleaned_data['generopsicologo_idgeneropsicologo']
#         tiposesion_ids = self.cleaned_data['tiposesion_idtiposesion']
#         corriente_ids = self.cleaned_data['corriente_idcorriente']
#         diagnostico_ids = self.cleaned_data['diagnostico_iddiagnostico']
#         motivosesion_ids = self.cleaned_data['motivosesion_idmotivosesion']
#         rangoprecio_ids = self.cleaned_data['rangoprecio_idrangoprecio']
#         coberturasalud_ids = self.cleaned_data['coberturasalud_id']

#         if commit:
#             instance.save()

#         instance.generopsicologo_idgeneropsicologo.set(Generopsicologo.objects.filter(idgeneropsicologo__in=generopsicologo_ids))
#         instance.tiposesion_idtiposesion.set(Tiposesion.objects.filter(idtiposesion__in=tiposesion_ids))
#         instance.corriente_idcorriente.set(Corrientepsicologica.objects.filter(idcorrientepsicologica__in=corriente_ids))
#         instance.diagnostico_iddiagnostico.set(Diagnostico.objects.filter(iddiagnostico__in=diagnostico_ids))
#         instance.motivosesion_idmotivosesion.set(Motivosesion.objects.filter(idmotivosesion__in=motivosesion_ids))
#         instance.rangoprecio_idrangoprecio.set(Rangoprecio.objects.filter(idrangoprecio__in=rangoprecio_ids))
#         instance.coberturasalud_id.set(Coberturasalud.objects.filter(idcoberturasalud__in=coberturasalud_ids))

#         return instance
    # def is_valid(self):
    
        
       
    #     generopsicologo_ids = self.cleaned_data['generopsicologo_idgeneropsicologo']
    #     tiposesion_ids = self.cleaned_data['tiposesion_idtiposesion']
    #     corriente_ids = self.cleaned_data['corriente_idcorriente']
    #     diagnostico_ids = self.cleaned_data['diagnostico_iddiagnostico']
    #     motivosesion_ids = self.cleaned_data['motivosesion_idmotivosesion']
    #     rangoprecio_ids = self.cleaned_data['rangoprecio_idrangoprecio']
    #     coberturasalud_ids = self.cleaned_data['coberturasalud_id']

    #     instance = super(FormTestPaciente, self).is_valid()

    #     instance.generopsicologo_idgeneropsicologo.set(Generopsicologo.objects.filter(idgeneropsicologo__in=generopsicologo_ids))
    #     instance.tiposesion_idtiposesion.set(Tiposesion.objects.filter(idtiposesion__in=tiposesion_ids))
    #     instance.corriente_idcorriente.set(Corrientepsicologica.objects.filter(idcorrientepsicologica__in=corriente_ids))
    #     instance.diagnostico_iddiagnostico.set(Diagnostico.objects.filter(iddiagnostico__in=diagnostico_ids))
    #     instance.motivosesion_idmotivosesion.set(Motivosesion.objects.filter(idmotivosesion__in=motivosesion_ids))
    #     instance.rangoprecio_idrangoprecio.set(Rangoprecio.objects.filter(idrangoprecio__in=rangoprecio_ids))
    #     instance.coberturasalud_id.set(Coberturasalud.objects.filter(idcoberturasalud__in=coberturasalud_ids))
    #     save = save(self, commit=True)
    #     if save(self, commit=True):
    #         instance.save()
    #     return instance
    

       
        

        
    # generopsicologo_idgeneropsicologo = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_genero,
    # )
    

    # tiposesion_idtiposesion = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_tiposesion,
    # )

    # corriente_idcorriente = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_corriente,
    # )

    # diagnostico_iddiagnostico = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_diagnostico,
    # )

    # motivosesion_idmotivosesion = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_motivo,
    # )

    # rangoprecio_idrangoprecio = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_precio,
    # )

    # coberturasalud_id = forms.MultipleChoiceField(
    #     required=True, 
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=get_cobertura,
    # )
    
    # def save(self, commit=True):
    #     instance = forms.ModelForm.save(self, commit=False)

    #     if commit:
    #         instance.save()

    #     # ... (resto del código para limpiar relaciones)

    #     # Agregar las relaciones con las instancias de los modelos
    #     for generopsicologo_id in self.cleaned_data['generopsicologo_idgeneropsicologo']:
    #         generopsicologo = Generopsicologo.objects.get(pk=generopsicologo_id)
    #         instance.generopsicologo_idgeneropsicologo.add(generopsicologo)
    #     for tiposesion_id in self.cleaned_data['tiposesion_idtiposesion']:
    #         tiposesion = Tiposesion.objects.get(pk=tiposesion_id)
    #         instance.tiposesion_idtiposesion.add(tiposesion)
    #     for corriente_id in self.cleaned_data['corriente_idcorriente']:
    #         corriente = Corrientepsicologica.objects.get(pk=corriente_id)
    #         instance.corriente_idcorriente.add(corriente)
    #     for motivosesion_id in self.cleaned_data['motivosesion_idmotivosesion']:
    #         motivosesion = Motivosesion.objects.get(pk=motivosesion_id)
    #         instance.motivosesion_idmotivosesion.add(motivosesion)
    #     for diagnostico_id in self.cleaned_data['diagnostico_iddiagnostico']:
    #         diagnostico = Diagnostico.objects.get(pk=diagnostico_id)
    #         instance.diagnostico_iddiagnostico.add(diagnostico)
    #     for rangoprecio_id in self.cleaned_data['rangoprecio_idrangoprecio']:
    #         rangoprecio = Rangoprecio.objects.get(pk=rangoprecio_id)
    #         instance.rangoprecio_idrangoprecio.add(rangoprecio)
    #     for cobertura_id in self.cleaned_data['coberturasalud_id']:
    #         cobertura = Coberturasalud.objects.get(pk=cobertura_id)
    #         instance.coberturasalud_id.add(cobertura)

    #     return instance

    