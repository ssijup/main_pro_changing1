from rest_framework import serializers
from netmagics.models import ActivityTracker


class ActivityTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityTracker
        fields = "__all__"

from rest_framework import serializers
from userapp.models import UserData
from userapp.serializers import UserSerializer
from .models import NetmagicsAdmin


class NetmagicsAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='user')   
    
    class Meta:
        model = NetmagicsAdmin
        fields = "__all__"



        