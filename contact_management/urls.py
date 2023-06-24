from django.urls import path
from .views import AddNewContactView, ContactUpdateView, ContactDeleteView

urlpatterns = [
    # Contact Management
    path('contact/create/', AddNewContactView.as_view(), name='contact_create'),
    path('contact/<int:pk>/edit/', ContactUpdateView.as_view(), name='edit_contact'),
    path('contact/<int:pk>/delete/', ContactDeleteView.as_view(), name='delete_contact'),
]