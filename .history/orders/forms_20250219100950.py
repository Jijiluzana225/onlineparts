

from django import forms
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'completename','email', 'phone_number', 'address' ]
        labels = {
            'completename': 'Full Name',
            'email': 'Email',
            'address': 'Ship to'
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'completename': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
