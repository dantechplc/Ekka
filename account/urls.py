from django.urls import path

from .views import *

app_name = 'account'

urlpatterns = [
    path('register', register_view, name='register'),
    path('register/verify/<uuid:token>', verify_user, name='verify_user'),
]
