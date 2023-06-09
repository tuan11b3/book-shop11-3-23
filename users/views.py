from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomForm
from store.models import Customer


# Create your views here.

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = CustomUserCreationForm
        form_2 = CustomForm
    else:
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)
        form_2 = CustomForm(request.POST or None)
        if all([form.is_valid(), form_2.is_valid()]):
            new_user = form.save()
            new_customer = form_2.save(commit=False)
            new_customer.user = new_user
            new_customer.name = new_user.username
            new_customer.save()
            #Log the user in and then redirect to home page.
            login(request, new_user)

            # user = request.user
            # customer, created = Customer.objects.get_or_create(user=user)
            #customer.email = request.user.email
            #customer.name = request.user.username

            #customer.save()
            return redirect('store:store')

    # Display a blank or invalid form
    context = {'form': form, 'form_2': form_2}
    return render(request, 'registration/register.html', context)
