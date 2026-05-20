from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, VendorEquipmentViewSet

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'manage', VendorEquipmentViewSet, basename='manage')  # Add this line for the vendor viewset

urlpatterns = [
    path('', include(router.urls)),
]