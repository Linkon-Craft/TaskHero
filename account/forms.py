
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")
