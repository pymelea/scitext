from time import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    password = models.CharField(max_length=150, blank=False)
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    address = models.TextField(default="", blank=True, null=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    cep = models.TextField(blank=True, null=True, default='')
    phone = models.CharField(max_length=30)
    city = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return self.username


class Environment(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Environment')
    capacity = models.IntegerField(verbose_name='Capacity of environment')
    address = models.CharField(max_length=150, verbose_name='Address')
    available = models.BooleanField(verbose_name='Available')
    description = models.TextField(verbose_name='Description of environment')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')

    class Meta:
        verbose_name = "Environment"
        verbose_name_plural = "Environments"
        ordering = ['available', 'description']

    def __str__(self):
        return self.name

    def is_available(self):
        if self.available == True:
            self.available.get_filter_kwargs_for_object(True)
        else:
            return self.available.get_filter_kwargs_for_object(False)


class Tenant(models.Model):
    name = models.CharField(max_length=150, verbose_name='Name of tenant')
    cpf = models.CharField(max_length=11, verbose_name='Tenant CPF')
    email = models.EmailField(verbose_name='Email', unique=True, blank=False)
    phone = models.IntegerField(verbose_name='Phone number')
    address = models.CharField(max_length=150, verbose_name='Tenant Address')
    fee_payment = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Fee')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Tenant Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Tenant Updated')

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return f"{self.name} {self.cpf} {self.email}"

    def is_pay(self):
        if self.fee_payment is not None:
            return True
        else:
            return False


class Booking(models.Model):
    name = models.CharField(max_length=150)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name='Tenant')
    env = models.ForeignKey(Environment, on_delete=models.CASCADE, verbose_name='Environment')
    cpf = models.CharField(max_length=11, verbose_name='CPF by responsable person', unique=True)
    fee = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Use Fee')
    real_value_pay = models.DecimalField(max_digits=9, decimal_places=2)
    capacity = models.IntegerField()
    days = models.CharField(max_length=1, choices=DAYS_OF_WEEK)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
