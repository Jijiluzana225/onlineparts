from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'orders/register.html', {'form': form})


def landing_page(request):
    return render(request, 'orders/landing.html') 

