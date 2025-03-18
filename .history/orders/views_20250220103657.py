from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
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
            return render(request, 'orders/landing.html', {'part_request': part_request})

    else:
        form = BidForm()

    return render(request, "orders/place_bid.html", {"form": form, "part_request": part_request})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import PartRequest

@method_decorator(login_required, name="dispatch")
class MyPartRequestsView(ListView):
    
    model = PartRequest
    template_name = "orders/my_part_requests.html"
    context_object_name = "part_requests"

    def get_queryset(self):
        return PartRequest.objects.filter(user=self.request.user).prefetch_related("bids").order_by("-created_at")



from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Bid

class BidDetailView(DetailView):
    model = Bid
    template_name = "orders/bid_detail.html"
    context_object_name = "bid"


from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Bid, PartRequest

class AcceptBidView(View):
    def post(self, request, pk):
        bid = get_object_or_404(Bid, pk=pk)
        part_request = bid.part_request

        # Close the PartRequest
        part_request.status = "Closed"
        part_request.save()

        # Set selected bid to "Accepted"
        bid.status = "Accepted"
        bid.save()

        # Reject all other bids for this part request
        Bid.objects.filter(part_request=part_request).exclude(pk=pk).update(status="Rejected")

        messages.success(request, "Bid accepted successfully! The part request is now closed.")
        return HttpResponseRedirect(reverse("my_part_requests"))



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Bid

@login_required
def store_bids(request):
    bids = Bid.objects.filter(store=request.user).order_by("-created_at")
    return render(request, "orders/store_bids.html", {"bids": bids})


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib import messages
from .models import Bid
from .forms import BidForm

class BidDetailViewView(DetailView):
    model = Bid
    template_name = "orders/bid_detail_view.html"
    context_object_name = "bid"

class BidUpdateView(UpdateView):
    model = Bid
    form_class = BidForm
    template_name = "orders/bid_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Bid updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("bid_detail", kwargs={"pk": self.object.pk})

class BidDeleteView(DeleteView):
    model = Bid
    template_name = "orders/bid_confirm_delete.html"
    success_url = reverse_lazy("store_bids")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Bid deleted successfully!")
        return super().delete(request, *args, **kwargs)
