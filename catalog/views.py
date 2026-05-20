from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Equipment
from .serializers import EquipmentSerializer
from .filters import EquipmentFilter
from .services import CatalogService  # Import your service

# 1. THE STUDENT VIEW (Current)
class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Students and Researchers use this to find gear."""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filterset_class = EquipmentFilter

# 2. THE VENDOR VIEW (New)
class VendorEquipmentViewSet(viewsets.ModelViewSet):
    """Vendors use this to manage their own gear via services."""
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated] # You can add IsVendor here

    def get_queryset(self):
        # Vendors only see/edit their own equipment
        return Equipment.objects.filter(vendor=self.request.user)

    def create(self, request, *args, **kwargs):
        # Extract serials for the service
        serial_numbers = request.data.pop('serial_numbers', [])
        
        # Standard DRF validation for the Equipment fields
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # CALL THE SERVICE: This is the bridge you were missing
            equipment = CatalogService.create_equipment_with_units(
                vendor=request.user,
                data=serializer.validated_data,
                serial_numbers=serial_numbers
            )
            
            output_serializer = self.get_serializer(equipment)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Handle business logic errors (e.g. duplicate serial numbers)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)