from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationViewSet, 
    UserProfileView, 
    UserListView, 
    VendorApprovalView
)

router = DefaultRouter()
# /api/users/register/ -> POST to create new account
router.register(r'register', UserRegistrationViewSet, basename='register')
# /api/users/list/ -> GET for admins to see all users
router.register(r'list', UserListView, basename='list')

urlpatterns = [
    # 1. Router paths (Register, List)
    path('', include(router.urls)),

    # 2. Authentication (Login & Refresh)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. Profiles
    path('profile/me/', UserProfileView.as_view(), name='profile'),

    # 4. Admin Gatekeeper: Approval for Vendors
    # Example: /api/users/approve-vendor/5/
    path('approve-vendor/<int:user_id>/', VendorApprovalView.as_view(), name='approve-vendor'),
]