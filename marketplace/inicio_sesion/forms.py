
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
	username = forms.CharField(
		label='Usuario o email',
		max_length=150,
		widget=forms.TextInput(attrs={'placeholder': 'Usuario o email'})
	)
	password = forms.CharField(
		label='Contraseña',
		widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
	)

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super().__init__(*args, **kwargs)

	def clean(self):
		cleaned = super().clean()
		username = cleaned.get('username')
		password = cleaned.get('password')
		if username and password:
			# Intentar autenticar con username; algunos proyectos usan email como username
			user = authenticate(username=username, password=password)
			if user is None:
				# Intentar autenticar por email si falla (si el backend lo soporta)
				try:
					from django.contrib.auth import get_user_model
					User = get_user_model()
					users = User.objects.filter(email__iexact=username)
					if users.exists():
						# si hay varios, intentar el primero
						user_obj = users.first()
						user = authenticate(username=user_obj.username, password=password)
				except Exception:
					user = None

			if user is None:
				raise forms.ValidationError('Usuario o contraseña incorrectos')
			if not user.is_active:
				raise forms.ValidationError('Cuenta inactiva')
			self.user_cache = user
		return cleaned

	def get_user(self):
		return self.user_cache
