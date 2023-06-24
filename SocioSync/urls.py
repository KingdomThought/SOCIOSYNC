
from user_auth.views import HomeView
from django.contrib import admin
from django.urls import path, include
#app_name = 'auth_user'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_auth/', include('user_auth.urls')),
    path('', HomeView.as_view(), name='home'),
    path('contact_management/', include('contact_management.urls')),
]