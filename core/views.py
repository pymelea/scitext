from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Environment, Booking, Category
from core.serializers import EnvironmentSerializer, BookingSerializer, CategorySerializer


# Create your views here.

# ViewSet for Environment
class EnvironmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Environment.objects.filter(available=True)
    serializer_class = EnvironmentSerializer

    # Filter systems
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_filters = ['available', 'name', 'cpf']
    ordering_fields = ['created']

    # Need Functions
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        return super(EnvironmentViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_owner() or user.is_superuser:
            return super(EnvironmentViewSet, self).create(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if (user.is_owner() and user.pk == self.get_object().user_env.pk) or user.is_superuser:
            return super(EnvironmentViewSet, self).update(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if (user.is_owner() and user.pk == self.get_object().user_env.pk) or user.is_superuser:
            return super(EnvironmentViewSet, self).destroy(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def get_all(self, request, *args, **kwargs):
        user = self.request.user
        if (user.is_owner() and user.pk == self.get_object().user_env.pk) or user.is_superuser:
            env = []
            for i in Environment.objects.filter(user_env=self.request.user):
                env.append(i.toJSON())
            return Response({"data": env}, status=status.HTTP_200_OK)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class BookingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)

    # Filters systems
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_filters = ['name', 'cpf', 'env', 'user_book', 'status']
    ordering_fields = ['get_status']

    # Need functions
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        return super(BookingViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.pk == self.get_object().user_book.pk or user.is_superuser:
            return super(BookingViewSet, self).create(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.pk == self.get_object().user_book.pk or user.is_superuser:
            return super(BookingViewSet, self).update(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.pk == self.get_object().user_book.pk or user.is_superuser:
            return super(BookingViewSet, self).destroy(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def get_booking_by_status(self, request, *args, **kwargs):
        user = self.request.user
        booking = []
        if user.is_client() or user.is_superuser:
            for i in Booking.objects.filter(status=True, user_book=user):
                booking.append(i.toJSON())
            return Response({"data": booking}, status=status.HTTP_200_OK)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )

    # Need Functions
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.pk == self.get_object().user_book.pk or user.is_superuser:
            return super(CategoryViewSet, self).create(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.pk == self.get_object().user_book.pk or user.is_superuser:
            return super(CategoryViewSet, self).update(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.pk == self.get_object().user_book.pk or user.is_superuser:
            return super(CategoryViewSet, self).destroy(request, *args, **kwargs)
        return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
