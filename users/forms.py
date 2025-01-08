from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=255, required=False)  # Add custom fields here
    city = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address', 'city']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
