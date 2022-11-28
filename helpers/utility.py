from django.core.mail import send_mail
from django.conf import settings


def send_verification_mail(token=None):
    send_mail(
        from_email='project@example.com',
        message=f'click on the link to activate your account. localhost:8000/account/register/verify/{token}',
        recipient_list=['get2dama11@gmail.com'],
        subject="Account Verification",
        fail_silently=False
    )
