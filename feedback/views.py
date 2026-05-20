from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EquipmentUnit, Feedback, IncidentReport
from .serializers import IncidentReportSerializer, FeedbackSerializer
from inventory.serializers import EquipmentUnitSerializer
from django.db.models import Count, Sum, Avg
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import IncidentReport
from transactions.models import Transaction
from transactions.models import Transaction


# --- 1. STUDENT FEEDBACK ---
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FeedbackSerializer
from .services import FeedbackService

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # CALL THE SERVICE
            feedback = FeedbackService.create_feedback(
                user=request.user,
                unit=serializer.validated_data['equipment_unit'],
                rating=serializer.validated_data['rating'],
                comment=serializer.validated_data.get('comment')
            )
            
            output_serializer = self.get_serializer(feedback)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

# --- 2. INCIDENT REPORTS ---
class IncidentReportViewSet(viewsets.ModelViewSet):
    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer
    # Usually, only staff/vendors can see all incident reports
    permission_classes = [permissions.IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        # The vendor/staff checking the item in is the reporter
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            incident_report = FeedbackService.create_incident_report(
                reporter=request.user,
                target_user=serializer.validated_data['target_user'],
                equipment_unit=serializer.validated_data['equipment_unit'],
                incident_type=serializer.validated_data['incident_type'],
                description=serializer.validated_data['description']
            )
            output_serializer = self.get_serializer(incident_report)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

class AdminDashboardAnalysisView(APIView):
    permission_classes = [IsAdminUser] # Only University Admins

    def get(self, request):
        # 1. Equipment Health Stats
        total_units = EquipmentUnit.objects.count()
        damaged_units = EquipmentUnit.objects.filter(status='DAMAGED').count()
        health_ratio = ((total_units - damaged_units) / total_units) * 100 if total_units > 0 else 0

        # 2. Financial Overview
        total_revenue = Transaction.objects.filter(status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0

        # 3. Risk Analysis (Vandalism vs Accidents)
        vandalism_count = IncidentReport.objects.filter(incident_type='VANDALISM').count()
        total_incidents = IncidentReport.objects.count()

        # 4. Student Reliability (High Risk Students)
        # Finds students with more than 2 incident reports
        risk_query = IncidentReport.objects.values('target_user__username').annotate(
            report_count=Count('id')
        ).filter(report_count__gt=2).order_by('-report_count')

        return Response({
            "fleet_health": {
                "total_units": total_units,
                "damaged_units": damaged_units,
                "health_percentage": round(health_ratio, 2)
            },
            "finance": {
                "total_revenue_kes": total_revenue,
            },
            "incidents": {
                "total_reports": total_incidents,
                "vandalism_cases": vandalism_count,
                "high_risk_students": risk_query
            },
            "pending_repairs": IncidentReport.objects.filter(resolved=False).count()
        })