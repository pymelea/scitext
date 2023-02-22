from rest_framework import serializers
from core.models import Environment, Booking, Category


# Serializers for Environment objects
class EnvironmentSerializer(serializers.ModelSerializer):
    """Environment serializer"""
    class Meta:
        model = Environment
        fields = ('name', 'capacity', 'address', 'available', 'description', 'created', 'updated', )

# Serializers for Bookings objects
class BookingSerializer(serializers.ModelSerializer):
    """Booking serializer"""

    class Meta:
        model = Booking
        fields = (
            'name', 'env', 'cpf', 'fee', 'real_value_pay', 'capacity', 'start_day', 'end_day', 'status'
        )


# Serializers for Categories objects
class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""

    class Meta:
        model = Category
        fields = ('name', 'description', 'created', 'updated', )

