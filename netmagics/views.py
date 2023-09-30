from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from impersonate.views import impersonate as django_impersonate

from django.http import HttpResponse
from .tasks import archive_old_records
from .models import NetmagicsAdmin
from userapp.models import UserData
from netmagics.models import ActivityTracker
from .serializer import NetmagicsAdminSerializer
from association.permissions import IsAuthenticatedNetmagicsAdmin, DeleteIsAuthenticatedNetmagicsAdmin
from .serializer import ActivityTrackerSerializer
from userapp.models import Advocate
from association.models import AdvocateAssociation, AssociationSuperAdmin, Association
from django.db.models import Q


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
        registrar = ActivityTracker.objects.all().order_by('-id')
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





# class ArchivingActivityTracterOldData(APIView):
#     def archive_records_view(request):
#         csv_path = archive_old_records()  # Call the function directly
#         with open(csv_path, 'r') as csvfile:
#             response = HttpResponse(csvfile.read(), content_type='text/csv')
#             response['Content-Disposition'] = f'attachment; filename="{csv_path.split("/")[-1]}"'
#             return response

from django.views import View
from django.http import HttpResponse, JsonResponse
import os


class ArchivingActivityTracterOldData(APIView):
    def get(self, request):
        try:
            csv_path, message = archive_old_records()  # Unpack the returned tuple
            print(csv_path,message,'555555555555555555555')
            if csv_path is None: # Check if the path is None
                return JsonResponse({"message": message})

            # If you want to provide a downloadable CSV:
            with open(csv_path, 'r') as csvfile:
                response = HttpResponse(csvfile.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{csv_path.split("/")[-1]}"'
                return response

        except Exception as e:
            # Print the current directory for debugging
            print("Current Directory:", os.getcwd())

            # Consider logging the exception for more detailed debugging
            # You can use Django's logging framework for this purpose:
            # import logging
            # logger = logging.getLogger(__name__)
            # logger.error(e)
            
            return JsonResponse({"error": str(e)})
        


# class LoginForParticularAssocitionUser(APIView):
#     def get(self, request, asso_id):
#         user = request.user
#         try:
#             association = Association.objects.get(id = asso_id)
#         except Association.DoesNotExist:
#             return Response({'message' : 'Association does not exist'}, status=status.HTTP_400_BAD_REQUEST)       
#         if AdvocateAssociation.objects.filter(advocate__user = user, association = association).exists() or AssociationSuperAdmin.objects.filter(user = user, association= association).exists :
#             return Response({'message' : 'User found relation with this association'}, status=status.HTTP_200_OK)
#         return Response({'message' : 'User not found in this association'}, status=status.HTTP_403_FORBIDDEN)


class LoginForParticularAssocitionUser(APIView):
    def get(self, request, asso_id):
        user = request.user
        try:
            association = Association.objects.get(id = asso_id)
        except Association.DoesNotExist:
            return Response({'message' : 'Association does not exist'}, status=status.HTTP_400_BAD_REQUEST)       
        if AssociationSuperAdmin.objects.filter(user = user).exists():
            if AssociationSuperAdmin.objects.filter(user = user, association= association).exists:
                return Response({'message' : 'User found asadmin with this association'}, status=status.HTTP_200_OK)
            return Response({'message' : 'User is not an admin of this association'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message' : 'User is global'}, status=status.HTTP_200_OK)



