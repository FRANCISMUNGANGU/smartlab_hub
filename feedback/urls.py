from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet, IncidentReportViewSet, AdminDashboardAnalysisView

router = DefaultRouter()
router.register(r'reviews', FeedbackViewSet, basename='feedback')
router.register(r'incidents', IncidentReportViewSet, basename='incident')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', AdminDashboardAnalysisView.as_view(), name='admin-analysis'),
]