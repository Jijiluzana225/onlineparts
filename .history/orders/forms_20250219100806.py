from django import forms
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['completename', 'emailaddress', 'address', 'password']
        labels = {
            'completename': 'Full Name',
            'email': 'Email',
            'address': 'Ship to'
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'completename': forms.TextInput(attrs={'class': 'form-control'}),
            'emailaddress': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
