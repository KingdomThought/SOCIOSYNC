from django.urls import path
from django.contrib import admin
from . import views
from .views import (
    HomeView,
    CustomLoginView, CustomLogoutView,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Home and Static Pages
    path('', HomeView.as_view(), name='home'),
    path('help/', views.help_view, name='help'),
    path('privacy_policy/', views.privacy_policy_view, name='privacy_policy'),
    path('about_us/', views.about_us_view, name='about_us'),
    path('contact_us/', views.contact_us_view, name='contact_us'),

    # Password Reset
    path('account/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Dynamic Pages
    path('dashboard/', views.dashboard_view, name='dashboard'),


    #path('admin/', admin.site.urls),
]