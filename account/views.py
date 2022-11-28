import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, reverse


from .forms import SignUpForm
from .models import Customer, Verify

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            print("form is valid oh")
            signup_form = signup_form.cleaned_data
            f_name = signup_form.get("firstname")
            l_name = signup_form.get("lastname")
            email = signup_form.get("email")
            phone = signup_form.get("phone_number")
            password = signup_form.get("password")
            try:
                user = User.objects.create(email=email)
            except User.IntegrityError:
                return render(request, "account/registration/register.html")
            else:
                user.set_password(password)
                user.is_customer = True
                user.is_active = True
                user.save()
                customer = Customer.objects.create(
                    user=user, first_name=f_name, last_name=l_name, mobile=phone)
                customer.save()
                obj = Verify.objects.create(user=user, token=uuid.uuid4())
                obj.save()
                return redirect('/')

    else:
        signup_form = SignUpForm()

    context = {'signup_form': signup_form}
    return render(request, "account/registration/register.html", context)


def verify_user(request, token):
    obj = Verify.objects.get(token=token)
    user = obj.user
    user.is_active = True  # change status to active to enable login
    user.save()
    del obj  # delete verify_instance after successful verification
    # return redirect(reverse('account:login'))  #to be implement
    return redirect('/')