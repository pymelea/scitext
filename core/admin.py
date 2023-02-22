from django.contrib import admin

from core.models import User, Environment, Booking, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Environment)
admin.site.register(Booking)
admin.site.register(Category)
