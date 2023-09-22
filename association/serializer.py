from rest_framework import serializers

from .models import (Association, Jurisdiction ,Court, MembershipPlan, MembershipFineAmount, 
                     Notification, AssociationMembershipPayment, AdvocateAssociation )
from userapp.models import Advocate, UserData
from advocates.serializer import UserSerializer
from .models import AssociationSuperAdmin
from association.models import Association
from advocates.serializer import NormalAdvocateSerializer


class CourtListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Court
        fields="__all__"

class AssociationListSerializer(serializers.ModelSerializer):
    court = CourtListSerializer(read_only=True) 
    court_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Court.objects.all(), source='court')
    class Meta:
        model = Association
        fields = "__all__"


class ListNormalAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Advocate
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('type_of_user') == 'normal_admin':
            return data
        return None

class ListSuperAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = AssociationSuperAdmin
        fields = "__all__"
 

class MembershipPlanSerializer(serializers.ModelSerializer):
    association = AssociationListSerializer(read_only=True) 
    association_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Association.objects.all(), source='association')
    class Meta:
        model = MembershipPlan
        fields = "__all__"

class MembershipFineAmountSerializer(serializers.ModelSerializer):
    association = AssociationListSerializer(read_only=True) 
    association_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Association.objects.all(), source='association')
    class Meta:
        model = MembershipFineAmount
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields="__all__"


class AssociationMembershipPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AssociationMembershipPayment
        fields="__all__"


class AdvocateAssociationSerializer(serializers.ModelSerializer):
    advocate = NormalAdvocateSerializer()
    association = AssociationListSerializer(read_only = True)
    approved_by = UserSerializer(read_only=True)
    class Meta:
        model=AdvocateAssociation
        fields="__all__"


class ListSuperAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='user')
    association = AssociationListSerializer(read_only=True) 
    association_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Association.objects.all(), source='association')
    class Meta:
        model = AssociationSuperAdmin
        fields = "__all__"


class MembershipApprovalSerilizer(serializers.ModelSerializer):
    advocate = NormalAdvocateSerializer(read_only=True)
    association = AssociationListSerializer(read_only = True)
    approved_by = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    auth_user_id = serializers.PrimaryKeyRelatedField(write_only = True,queryset=UserData.objects.all(), source='approved_by')
    class Meta:
        model=AdvocateAssociation
        fields="__all__" 
