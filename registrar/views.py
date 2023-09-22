from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import status
from .serializer import RegistrarSerializer
from userapp.models import Registrar,UserData
from association.models import Court

from association.permissions import IsAuthenticatedNetmagicsAdmin, IsAuthenticatedRegistrar


class RegistrarView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def get(self, request):
        registrar = Registrar.objects.all()
        serializer = RegistrarSerializer(registrar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateRegistrarView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def post(self, request, court_id):      
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        try:
            court = Court.objects.get(id=court_id)
            print("yyyy",court.id)
        except Court.DoesNotExist:
             return Response({"message" :"Court could not be found"})
        user = UserData.objects.create_user(email=email, password=password,name=name)
        data = request.data.copy()
        data['user_id'] = user.id
        data['court_id'] = court_id
        serializer = RegistrarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({" message": "Registrar successfully created"}, status=status.HTTP_201_CREATED)
        return Response({"message": "validation failed"}, status=status.HTTP_400_BAD_REQUEST) 

    
class DeleteRegistrarView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def delete(self, request, id):
        try:
            registrar = Registrar.objects.get(id=id)
        except Registrar.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        registrar.delete()
        return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class EditRegistrarView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin | IsAuthenticatedRegistrar]

    def patch(self, request, id):
        try:
            registrar = Registrar.objects.get(id=id)
            print("uuuuuuuuuuuu",registrar)
        except Registrar.DoesNotExist:
            return Response({"message": "Registrar could not be found"}, status=status.HTTP_404_NOT_FOUND)
        new_name = request.data.get('name')
        if new_name:
            registrar.user.name = new_name
            registrar.save()
        serializer = RegistrarSerializer(registrar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Validation failed... Please try again"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class EditFormViewRegistrarView(APIView):
    def get(self, request, id) :
        try:
            registrar=Registrar.objects.get(id=id)
            serializer=RegistrarSerializer(registrar)
            return Response(serializer.data ,status=status.HTTP_200_OK)

        except Registrar.DoesNotExist:
                    return Response({
                         "message" : "Registrar  could not be found"
                         },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                    return Response({
                        "message": "An unexpected error occurred "
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class RegistrarCountView(APIView):
    def get(self, request):
        registar_count = Registrar.objects.count()
        return Response({'registar_count': registar_count}, status=status.HTTP_200_OK)


 