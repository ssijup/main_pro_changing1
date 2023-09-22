from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from impersonate.views import impersonate as django_impersonate


from .models import NetmagicsAdmin
from userapp.models import UserData
from netmagics.models import ActivityTracker
from .serializer import NetmagicsAdminSerializer
from association.permissions import IsAuthenticatedNetmagicsAdmin, DeleteIsAuthenticatedNetmagicsAdmin
from .serializer import ActivityTrackerSerializer

class NetmagicsAdminCreateView(APIView):
    def post(self , request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        user = UserData.objects.create_user(email=email, password=password, name=name)

        data = request.data.copy()  
        data['user_id'] = user.id
        serializer = NetmagicsAdminSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "validation failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListNetmagicsAdmin(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def get(self, request):
        print(request)
        user=request.user
        print("sijuuuuuuuuuuu :", user)
        val = NetmagicsAdmin.objects.get(user=user)
        print(val ,"tttttttttttt")
        admins = NetmagicsAdmin.objects.all()
        serializer = NetmagicsAdminSerializer(admins, many =True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class DeleteNetmagicsAdmin(APIView):
    # permission_classes = [DeleteIsAuthenticatedNetmagicsAdmin]
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def delete(self, request, id):
        try:
            admin=NetmagicsAdmin.objects.get(id=id)
            admin.delete()
            return Response({"message" : "Admin Removed successfully"})
        
        except NetmagicsAdmin.DoesNotExist:
            return Response({"message" : "Admin could not be found"})
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred .Please try again later"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AcivityTrackerView(APIView):
    def get(self, request):
        registrar = ActivityTracker.objects.all()
        serializer = ActivityTrackerSerializer(registrar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class StartImpersonatingByNetmagicsAdmin(APIView):
    permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def get(self, request, id):
        print("pppppp ",request.user )
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        response = django_impersonate(request, id)
        print(response)

        if response.status_code == 302:
            print("siju impersonating", id)
            return Response({"message": "impersonation started"})
        return Response({"message": "You are not allowed for this action"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class StopImpersonatingByNetmagicsAdmin(APIView):
    def post(self, request, id):
        response = django_impersonate(request, id)
        if response.status_code == 302:
            return Response({"message": "impersonation stopped"})
        return Response({"message": "You are not allowed for this action"}, status=status.HTTP_406_NOT_ACCEPTABLE)

