from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    PUBLIC_ROLES = [
        User.Roles.RESEARCHER,
        User.Roles.STUDENT,
        User.Roles.VENDOR,
    ]

    role = serializers.ChoiceField(choices=User.Roles.choices, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'phone', 'organization', 'pickup_location', 'dropoff_location',
            'profile_picture', 'is_active', 'date_joined'
        ]
        read_only_fields = ['date_joined', 'is_active']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'required': True},
        }

    def validate_role(self, value):
        if value not in self.PUBLIC_ROLES:
            raise serializers.ValidationError("Invalid role. Role must be one of: Researcher, Student, Vendor.")
        return value
    

    