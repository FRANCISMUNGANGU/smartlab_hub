from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register(r'transaction-history', TransactionViewSet, basename='transaction')
urlpatterns = [
    path('', include(router.urls)),
]

