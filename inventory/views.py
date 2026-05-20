from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EquipmentUnit
from .serializers import EquipmentUnitSerializer
from .services import InventoryService
from .permission import IsEquipmentManager

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = EquipmentUnit.objects.all()
    serializer_class = EquipmentUnitSerializer
    permission_classes = [IsEquipmentManager]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'VENDOR':
            return EquipmentUnit.objects.filter(equipment__vendor=user)
        return EquipmentUnit.objects.filter(status='AVAILABLE') 

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        unit = self.get_object()
        has_damage = request.data.get('has_damage', False)
        description = request.data.get('description')

        try:
            student = InventoryService.process_check_in(
                unit=unit,
                vendor=request.user,
                has_damage=has_damage,
                description=description
            )
            
            msg = f"Check-in successful. Unit is {unit.status}."
            if has_damage:
                msg += f" Incident filed against {student.username}."
            
            return Response({"status": msg}, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)