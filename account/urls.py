from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path('register', register_view, name='register'),
    path('login', login_view, name='login'),
    path("activate/<slug:uidb64>/<slug:token>/", account_activate, name="activate"),
]
