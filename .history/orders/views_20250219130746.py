from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)  # Authenticate
            if user is not None:
                login(request, user)  # Auto-login user
                return redirect("landing")  # Redirect to landing page
    else:
        form = UserCreationForm()
    
    return render(request, "orders/register.html", {"form": form})


def landing_page(request):
    return render(request, 'orders/landing.html') 



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomerUpdateForm

@login_required
def profile_update_view(request):
    user = request.user
    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile_update")  # Stay on profile page after saving
    else:
        form = CustomerUpdateForm(instance=user)

    return render(request, "orders/profile_update.html", {"form": form})

