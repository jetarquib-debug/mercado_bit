from django import forms
from usuario.models import Usuario
from tienda.models import Tienda


class UsuarioRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = Usuario
        # incluir todos los atributos no automáticos
        fields = [
            'nombres', 'apellidos', 'email', 'imagenes',
            'codigo_pais', 'telefono', 'direccion', 'pais', 'departamento', 'provincia', 'distrito', 'sexo', 'dni_ce'
        ]
        # Nota: no incluimos el campo de modelo `contrasena` aquí porque
        # usamos los campos auxiliares `password1` y `password2` para la
        # entrada/validación de contraseña en el formulario. La contraseña
        # final se asigna en `save()`.

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este email.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # usar el password1 para la contraseña final
        password = self.cleaned_data.get('password1')
        if password:
            usuario.contrasena = password
        # La validación del teléfono frente al código de país se realiza en clean_telefono()
        if commit:
            usuario.save()
            # guardar ManyToMany
            if self.cleaned_data.get('imagenes'):
                usuario.imagenes.set(self.cleaned_data.get('imagenes'))
        return usuario

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        codigo = self.cleaned_data.get('codigo_pais')
        if telefono and not codigo:
            raise forms.ValidationError("Debe seleccionar un código de país antes de ingresar el teléfono.")
        return telefono


class TiendaRegistrationForm(forms.ModelForm):
    class Meta:
        model = Tienda
        # todos los atributos no automaticos (excluye fecha_registro y otras automaticas)
        fields = [
            'nombre_tienda', 'descripcion', 'email', 'codigo_pais', 'telefono',
            'direccion', 'distrito', 'provincia', 'departamento', 'pais', 'ruc', 'imagenes'
        ]

    def save(self, usuario, commit=True):
        tienda = super().save(commit=False)
        tienda.usuario = usuario
        if commit:
            tienda.save()
            if self.cleaned_data.get('imagenes'):
                tienda.imagenes.set(self.cleaned_data.get('imagenes'))
        return tienda

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        codigo = self.cleaned_data.get('codigo_pais')
        if telefono and not codigo:
            raise forms.ValidationError("Debe seleccionar un código de país antes de ingresar el teléfono de la tienda.")
        return telefono
