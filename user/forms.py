from user.models import User
from django.forms import *

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'}) 
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        template_name = 'user/list.html'
        fields = ['first_name','last_name','username', 'email', 'password', 'groups']
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Nombre',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Apellidos',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Ingrese su nombre de Usuario',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Correo Electrónico',
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'placeholder': 'Ingrese su contraseña',
                }
            ),
            'groups': Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'placeholder': "Seleccione un rol",
            })
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']
        
def save(self, commit=True):
    u = super().save(commit=False)
    pwd = self.cleaned_data.get('password')
    
    # Si es creación, se le asigna la contraseña
    if u.pk is None:
        u.set_password(pwd)
    else:
        # Comparamos (esto puede mejorarse, ya que la contraseña está en hash)
        if u.password != pwd:
            u.set_password(pwd)
    
    if commit:
        u.save()
        # Asignación limpia de grupos: esto actualizará incluso si la lista está vacía
        u.groups.set(self.cleaned_data.get('groups'))
    return u
