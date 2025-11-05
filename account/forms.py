
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()



class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    email = forms.EmailField(max_length=254, required=True, help_text="Required. Enter a valid email address.")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) < 3:
            raise forms.ValidationError("First name must be at least 3 characters long.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) < 3:
            raise forms.ValidationError("Last name must be at least 3 characters long.")
        return last_name
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")
