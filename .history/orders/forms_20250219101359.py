from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'completename','email', 'phone_number', 'address' ]

        labels = {
            'completename': 'Full Name',
            'email': 'Email',
            'address': 'Ship to'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'completename': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }