from django.db import transaction
from .models import User
from alerts.models import NotificationLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserService:
    @staticmethod    
    @transaction.atomic
    def register_user(validated_data):
        password = validated_data.pop('password')
        role = validated_data.get('role')

        # Create user with the password correctly handled in one go
        user = User.objects.create_user(password=password, **validated_data)

        welcome_message = f"Welcome to SmartLab Hub, {user.first_name}!"
        if role == User.Roles.VENDOR:
            user.is_active = False 
            welcome_message += " Your vendor account is pending administrative approval."
            
            # Notify all Admins safely (avoiding .get() crash)
            admins = User.objects.filter(role='ADMIN', is_staff=True)
            for admin in admins:
                NotificationLog.objects.create(
                    user=admin,
                    alert_type="SYSTEM",
                    message=f"New Vendor Registration: {user.username} from {user.organization}. Verification required."
                )
        else:
            welcome_message += f" Your account as a {user.role} is now active."

        NotificationLog.objects.create(
            user=user,
            alert_type="INFO",
            message=welcome_message
        )

        return user



    @staticmethod
    @transaction.atomic
    def update_user_role(user_id, new_role):
        user = User.objects.select_for_update().get(id=user_id)
        old_role = user.role
        user.role = new_role
        user.save()

        # Notify the user about their role change
        NotificationLog.objects.create(
            user=user,
            alert_type="ROLE_CHANGE",
            message=f"Your role has been updated from {old_role} to {new_role}."
        )

        return user
    


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims to the response
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['full_name'] = f"{self.user.first_name} {self.user.last_name}"
        
        return data