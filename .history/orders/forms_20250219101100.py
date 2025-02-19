from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea, required=False)

    labels = {
            'completename': 'Full Name',
            'email': 'Email',
            'address': 'Ship to'
        }
    class Meta:
        model = Customer
        
