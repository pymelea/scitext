from .views import EnvironmentViewSet, BookingViewSet, CategoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('api/env', EnvironmentViewSet, 'env')
router.register('api/booking', BookingViewSet, 'booking')
router.register('api/category', CategoryViewSet, 'category')

urlpatterns = router.urls

