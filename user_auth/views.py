from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
                                       PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django import forms

from .forms import CustomUserCreationForm
from contact_management.models import Contact
from .models import CustomUser
from django.core.paginator import Paginator


@login_required
def dashboard_view(request):
    # Get only the contacts created by the logged-in user
    contact_list = Contact.objects.filter(user=request.user)
    paginator = Paginator(contact_list, 10)  # Show 10 contacts per page.

    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {'contacts': contacts})

# Login Registration Authentication and Logout
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')  # get the username from the form
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'A user with that email already exists.')
            elif CustomUser.objects.filter(username=username).exists():  # check if the username is already in use
                form.add_error('username', 'A user with that username already exists.')
            else:
                form.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=255)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


# Static Page Views
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'user_auth/home.html')


def contact_us_view(request):
    return render(request, 'contact_us.html')


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')


def about_us_view(request):
    return render(request, 'about_us.html')


def help_view(request):
    return render(request, 'help.html')


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'

    def get_success_url(self):
        return reverse_lazy('login')



