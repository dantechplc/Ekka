from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm
from .models import Customer, Verify

User = get_user_model()


def register_view(request):
    """" Register view for customer """

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            print("form is valid oh")
            signup_form = signup_form.cleaned_data
            f_name = signup_form.get("firstname")
            l_name = signup_form.get("lastname")
            email = signup_form.get("email")
            phone = signup_form.get("mobile")
            password = signup_form.get("password2")

            # Creating user and customer instances
            user.set_password(password)
            user.is_active = False
            user.is_customer = True
            user.save()
            customer = Customer.objects.create(
                user=user, first_name=f_name, last_name=l_name, mobile=phone)
            customer.save()

            # Sending customer verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": f_name,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            name = f_name
            messages.success(request,
                             '. A verification email has been sent to your '
                             'email address, verify your account then '
                             'proceed with login ')
            email = EmailMultiAlternatives(
                mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, 'text/html')
            email.content_subtype = 'html'
            email.mixed_subtype = 'related'
            email.send()
            return redirect('account:register')

            # else:
            #     user.set_password(password)
            #     user.is_customer = True
            #     user.save()
            #     customer = Customer.objects.create(
            #         user=user, first_name=f_name, last_name=l_name, mobile=phone)
            #     customer.save()
            #     gen_token = uuid.uuid4()
            #     obj = Verify.objects.create(user=user, token=gen_token)
            #     obj.save()
            #     send_verification_mail(token=gen_token)
            #     return redirect('/')

    else:
        signup_form = SignUpForm()
        context = {'signup_form': signup_form}
        return render(request, "account/registration/register.html", context)

    return render(request, "account/registration/register.html", {'signup_form': signup_form})


def verify_user(request, token):
    obj = Verify.objects.get(token=token)
    user = obj.user
    user.is_active = True  # change status to active to enable login
    user.save()
    del obj  # delete verify_instance after successful verification
    # return redirect(reverse('account:login'))  #to be implement
    return redirect('/')


def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # render(request, 'accounts/successful.html') we use this later to present the user with a nice activation
        # successful message
        return HttpResponse('account activated successfully')
    else:
        return HttpResponse('account activated successfully')  # render(request, 'accounts/failure.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        valuenext = request.GET.get('next')  # get the specific url from request

        user = authenticate(request, email=username, password=password)

        if user is not None and user.is_staff != True:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Email or Password is incorrect')

    return render(request, 'account/login.html')
