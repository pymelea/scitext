from time import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import fields
from django.utils.timezone import now

# Create your models here.

STATUS = (
    ('0', 'Not Used'),
    ('1', 'Used'),
    ('2', 'Pendings'),
)

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
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    phone = models.CharField(max_length=30, verbose_name='Phone number')
    address = models.CharField(max_length=150, verbose_name='Address')
    city = models.CharField(max_length=150, blank=True, null=True)
    cep = models.CharField(max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def is_client(self):
        for group in self.groups.all():
            if group.name == "Client":
                return True
        return False

    def is_owner(self):
        for group in self.groups.all():
            if group.name == "Owner":
                return True
        return False

    def toJSON(self):
        return {
            'name': self.get_full_name(),
            'username': self.username,
            'email': self.email,
            'cpf': self.cpf,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'cep': self.cep,
            'created': self.created,
            'updated': self.updated,
        }


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


class Environment(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Environment')
    capacity = models.IntegerField(verbose_name='Capacity of environment')
    address = models.CharField(max_length=150, verbose_name='Address')
    available = models.BooleanField(verbose_name='Available')
    description = models.TextField(verbose_name='Description of environment')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    user_env = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Environment"
        verbose_name_plural = "Environments"
        ordering = ['available', 'address', 'description', ]

    def __str__(self):
        return self.name

    def toJSON(self):
        return {
            'name': self.name,
            'capacity': self.capacity,
            'address': self.address,
            'available': self.available,
            'description': self.description,
            'created': self.created.isoformat(),
            'updated': self.updated,
            'user': self.user_env.toJSON(),
        }


class Booking(models.Model):
    name = models.CharField(max_length=150)
    env = models.ForeignKey(Environment, on_delete=models.CASCADE, verbose_name='Environment')
    cpf = models.CharField(max_length=15, verbose_name='CPF by responsable person', unique=True)
    fee = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Use Fee')
    real_value_pay = models.DecimalField(max_digits=9, decimal_places=2)
    capacity = models.IntegerField()
    start_day = models.DateField()
    end_day = models.DateField()
    user_book = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(verbose_name='Are you ready for do the booking?')

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return self.name

    def toJSON(self):
        return {
            'name': self.name,
            'env': self.env.toJSON(),
            'cpf': self.cpf,
            'fee': self.fee,
            'real_value_pay': self.real_value_pay,
            'capacity': self.capacity,
            'start_day': self.start_day,
            'end_day': self.end_day,
            'user_book': self.user_book.toJSON(),
            'created': self.created,
            'updated': self.updated,
            'status': self.status
        }

    def is_pay(self):
        return self.fee is not None
