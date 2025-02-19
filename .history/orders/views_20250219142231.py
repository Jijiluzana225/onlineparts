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
            return redirect("home")  # Stay on profile page after saving
    else:
        form = CustomerUpdateForm(instance=user)

    return render(request, "orders/profile_update.html", {"form": form})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PartRequestForm

@login_required
def order_part_view(request):
    if request.method == "POST":
        form = PartRequestForm(request.POST, request.FILES)
        if form.is_valid():
            part_request = form.save(commit=False)
            part_request.user = request.user
            part_request.save()
            return redirect("order_success")  # Redirect to a success page
    else:
        form = PartRequestForm()

    return render(request, "orders/order_part.html", {"form": form})


def order_success(request):
    return render(request, "orders/order_success.html")

from django.shortcuts import render
from .models import PartRequest

def part_request_list(request):
    part_requests = PartRequest.objects.all().order_by('-created_at')  # Order by latest date
    return render(request, 'orders/part_request_list.html', {'part_requests': part_requests})

from django.shortcuts import render, get_object_or_404
from .models import PartRequest

def part_request_detail(request, pk):
    part_request = get_object_or_404(PartRequest, pk=pk)
    return render(request, 'orders/part_request_detail.html', {'part_request': part_request})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PartRequest, Bid
from .forms import BidForm

@login_required
def place_bid(request, part_request_id):
    part_request = get_object_or_404(PartRequest, id=part_request_id)

    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.part_request = part_request
            bid.store = request.user  # Only logged-in stores can bid
            bid.save()
            return redirect("part_request_detail", part_request_id=part_request.id)  # Redirect to details page

    else:
        form = BidForm()

    return render(request, "bids/place_bid.html", {"form": form, "part_request": part_request})
