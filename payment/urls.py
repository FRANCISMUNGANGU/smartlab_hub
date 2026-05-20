from django.urls import path, include

from .views import PaystackWebhookView, PaystackCallbackView


urlpatterns = [
    path('callback/', PaystackCallbackView.as_view(), name='paystack-callback'),
    path('webhook/', PaystackWebhookView.as_view(), name='paystack-webhook'),
]