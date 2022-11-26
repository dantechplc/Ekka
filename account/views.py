# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


def register_view(request):
    return render(request, "account/registration/register.html")
