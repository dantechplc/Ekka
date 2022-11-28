# Create your models here.
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from account.manager import UserManager
from helpers.models import TrackingModel


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return str(self.email)


class Customer(TrackingModel, models.Model):
    user = models.OneToOneField(User, verbose_name="Customer", related_name='customer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=150)

    def str(self):
        return str(self.user)

    class Meta:
        verbose_name = "Customer"


class Vendor(TrackingModel, models.Model):
    user = models.OneToOneField(User, verbose_name='Vendor', related_name='vendor', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=150)
    brand_name = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to='vendor/profile_pic', default='avatars/avatar.jpg', blank=True)
    profile_pic_thumbnail = ImageSpecField(source='profile_pic',
                                           processors=[ResizeToFill(80, 80)],
                                           format="JPEG",
                                           options={'quality': 60})

    def str(self):
        return str(self.user)

    class Meta:
        verbose_name = "Vendor"


class Address(TrackingModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("last Name"), max_length=150)
    mobile = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address = models.CharField(_("Address"), max_length=255)
    town_city = models.CharField(_("Town/City"), max_length=150)
    state = models.CharField(_("State"), max_length=150)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return str(self.customer)


class Verify(models.Model):
    user = models.ForeignKey(User, related_name='verify_handle', on_delete=models.CASCADE)
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.token}'
