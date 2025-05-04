from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(max_length=512, required=True)
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'full_name': self.validated_data.get('full_name', ''),
            'role': self.validated_data.get('role', 'USER'),

        })
        return data

    def save(self, request):
        user = super().save(request)
        user.full_name = self.validated_data.get('full_name')
        user.role = self.validated_data.get('role')
        user.username = self.validated_data.get('username')
        user.save()
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'role',
                  'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'is_active', 'is_staff']
