from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    is_store = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Register as a Store"
    )
    phone_number = forms.CharField(        
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        label="Phone Number"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your Complete address'}),
        required=False,
        label="Complete Address"
    )

    class Meta:
        model = Customer
        fields = ['is_store','username', 'password1', 'password2', 'completename', 'email', 'phone_number', 'address']

        labels = {
            'completename': 'Full Name / Store Name',
            'email': 'Email',
            'address': 'Complete Address',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter password', 
                'autocomplete': 'new-password', 
                'minlength': '8'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Confirm password', 
                'autocomplete': 'new-password', 
                'minlength': '8'
            }),
            'completename': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }


from django import forms
from .models import Customer

class CustomerUpdateForm(forms.ModelForm):
    is_store = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Register as a Store"
    )
    class Meta:
        model = Customer
        fields = ["is_store", "completename", "phone_number", "address"]
        labels = {
            'completename': 'Full Name / Store Name',
            'email': 'Email',
            'address': 'Complete Address',
        }
        widgets = {
            "completename": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
