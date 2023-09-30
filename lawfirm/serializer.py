from rest_framework import serializers

from .models import LawFirm, AdvocateLawfirm, LawfirmNotification
from userapp.models import Advocate
from advocates.serializer import NormalAdvocateSerializer




class LawFirmListSerializer(serializers.ModelSerializer):
    # advocate = AdvocateLawfirmSerializer(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Advocate.objects.all())
    class Meta:
        model = LawFirm
        fields = "__all__"


class LawFirmNotificationSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = LawfirmNotification
        fields = "__all__"





class AdvocateLawfirmSerializer(serializers.ModelSerializer):
    lawfirm = LawFirmListSerializer()
    advocate = NormalAdvocateSerializer()
    
    class Meta:
        model = AdvocateLawfirm
        fields = "__all__"
