from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

# Klasa obsługująca formularz rejestracji
class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Pole wymagane. Podaj poprawny adres email.')

	# Meta klasa zarządzająca modelem
	class Meta:
		model = Account
		fields = ("email", "username", "password1", "password2")

# Klasa obsługująca autentyfikacje
class AccountAuthenticationForm(forms.ModelForm):
	
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	# Meta klasa zarządzająca modelem
	class Meta:
		model = Account
		fields = ('email', 'password')
	# Funkcja sprawdzająca poprawność danych użytkownika przed autentyfikacją
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Niewłaściwy login")

# Klasa obsługująca formularz zarządzania kontem
class AccountUpdateForm(forms.ModelForm):
	# Meta klasa zarządzająca modelem
	class Meta:
		model = Account
		fields = ('email', 'username')
	# Funkcja sprawdzająca czy podany email jest unikalny
	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" jest już w użytku.' % email)
	# Funkcja sprawdzająca czy podana nazwa użytkownika jest unikalna
	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Nazwa użytkownika "%s" jest już w użytku.' % username)