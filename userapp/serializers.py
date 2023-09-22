from rest_framework import serializers
from .models import UserData, Advocate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Include the email in the token's payload
        token['email'] = user.email

        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = "__all__"


    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)