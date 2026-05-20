from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NotificationLog
from .serializers import NotificationLogSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and marking notifications as read.
    """
    serializer_class = NotificationLogSerializer
    

    def get_queryset(self):
        # Users only see their own alerts
        return NotificationLog.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'all notifications marked as read'}, status=status.HTTP_200_OK)