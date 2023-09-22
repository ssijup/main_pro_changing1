from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from association.permissions import IsAuthenticatedNetmagicsAdmin, IsAuthenticatedAssociationAdmin
from .serializer import NormalAdvocateSerializer
from lawfirm.permissions import IsAuthenticatedLawfirmAdmin
from .permissions import IsAuthenticatedAdvocate
from rest_framework import serializers
from userapp.models import Advocate,UserData
from association.models import AssociationMembershipPayment, AdvocateAssociation
from lawfirm.models import AdvocateLawfirm
from association.serializer import AdvocateAssociationSerializer
from lawfirm.serializer import AdvocateLawfirmSerializer
from association.serializer import AssociationMembershipPaymentSerializer

class AdvocatesListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        normal_advocate = Advocate.objects.filter(type_of_user='normal_advocate')
        serializer = NormalAdvocateSerializer(normal_advocate, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateAdvocatesListView(APIView):
    def post(self, request):        
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        user = UserData.objects.create_user(email=email, password=password, name=name)
        
        data = request.data.copy()  
        data['user_id'] = user.id  
        data['type_of_user'] = 'normal_advocate'

        serializer = NormalAdvocateSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"message": "validation failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class SuspendAdvocateView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin | IsAuthenticatedAssociationAdmin | IsAuthenticatedLawfirmAdmin]

    def patch(self, request, id):
        try :
            advocate = Advocate.objects.get(id = id)
            serializer=NormalAdvocateSerializer(advocate)
            advocate.is_suspend = not advocate.is_suspend
            advocate.save()

            if advocate.is_suspend:
                return Response({"message" : "Advocate suspended successfully" ,"data":serializer.data}, status = status.HTTP_202_ACCEPTED)
            return Response({"message" : "Advocate suspension removed successfully" ,"data":serializer.data}, status = status.HTTP_202_ACCEPTED)

        except Advocate.DoesNotExist:
            return Response({
                "message" : "Advocate does not found"
                }, status= status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred "
                
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    

class EditAdvocateProfileView(APIView):
    permission_classes = [IsAuthenticatedNetmagicsAdmin | IsAuthenticatedAdvocate]

    def patch(self, request, id): 
        try:
            advocate=Advocate.objects.get(id=id) 
            #Editing UserData Model    
            name = request.data.get('name')
            if name is not None:
                UserData.objects.filter(id=advocate.user.id).update(name=name)
            # request.data['user'] = advocate.user.id
            #Editing Advocates Model
            serializer = NormalAdvocateSerializer(advocate, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Advocate details updated sucessfully"},status=status.HTTP_200_OK)
            print(serializer._errors)
            return Response({"message" : "Validation error"},status=status.HTTP_400_BAD_REQUEST)
        except Advocate.DoesNotExist:
            return Response({"message" : "Advocate could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message" : "An unexcepted error occured "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class AdvocateEditFormView(APIView):
    def get(self, request, id) :
        try:
            advocate=Advocate.objects.get(id=id)
            serializer=NormalAdvocateSerializer(advocate)
            return Response(serializer.data ,status=status.HTTP_200_OK)

        except Advocate.DoesNotExist:
                    return Response({
                         "message" : "Advocate  could not be found"
                         },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                    return Response({
                        "message": "An unexpected error occurred "  
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdvocatesPaymentView(APIView):
    def get(self, request,id):
        advocate = AssociationMembershipPayment.objects.filter(for_user_details__id=id)
        serializer = AssociationMembershipPaymentSerializer(advocate, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AssociationAdvocateViewUsingID(APIView):
    def get(self, request,id):
        # user= request.user
        # auth_user = AssociationSuperAdmin.objects.get(user = user)
        # association = auth_user.association
        association = AdvocateAssociation.objects.filter(advocate__id=id)
        serializer = AdvocateAssociationSerializer(association, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AssociationAdvocateView(APIView):
    def get(self, request):
        user= request.user
        # auth_user = AssociationSuperAdmin.objects.get(user = user)
        # association = auth_user.association
        association = AdvocateAssociation.objects.filter(advocate__user=user)
        serializer = AdvocateAssociationSerializer(association, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AdvocateLawFirmListView(APIView):
    def get(self, request, id):
        advocates = AdvocateLawfirm.objects.filter(lawfirm__id=id)
        serializer = AdvocateLawfirmSerializer(advocates, many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    
class DeleteAdvocateLawFirmView(APIView):
    def delete(self, request, id):
        try:
            advocates=AdvocateLawfirm.objects.get(lawfirm__id=id)
            advocates.delete()
            return Response({"message" : "LawFirm deleted sucessfully"})
        
        except AdvocateLawfirm.DoesNotExist:
            return Response({"message" : "The LawFirm cout not be found"})
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvocateMembershipsViewUsingID(APIView):
    def get(self, request,id):
        payments = AssociationMembershipPayment.objects.get(for_user_details__user__id = id)
        serializer = AssociationMembershipPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdvocateMembershipsView(APIView):
    def get(self, request):
        user= request.user
        payments = AssociationMembershipPayment.objects.get(for_user_details__user = user)
        serializer = AssociationMembershipPaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdvocatesProfileView(APIView):
    def get(self, request):
        user = request.user
        try:
            advocate = Advocate.objects.get(user=user)
        except Advocate.DoesNotExist:
            return Response({"detail": "Advocate not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NormalAdvocateSerializer(advocate)
        return Response(serializer.data, status=status.HTTP_200_OK)


