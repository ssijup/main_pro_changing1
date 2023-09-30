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
from association.models import RawData, AssociationMembershipPayment, AdvocateAssociation
from lawfirm.models import AdvocateLawfirm
from association.serializer import AdvocateAssociationSerializer
from lawfirm.serializer import AdvocateLawfirmSerializer
from association.serializer import AssociationMembershipPaymentSerializer




class AdvocatesListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        normal_advocate = Advocate.objects.filter(type_of_user='normal_advocate')
        serializer = NormalAdvocateSerializer(normal_advocate, many=True, context = {'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateAdvocatesListView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        enrollment_id = request.data.get('enrollment_id')
        if UserData.objects.filter(enrollment_id = enrollment_id).exists():
            return Response({'message' : 'Enrollment ID alredy exists..'}, status=status.HTTP_400_BAD_REQUEST)
        if UserData.objects.filter(email = email).exists():
            return Response({'message' : 'Email alredy exists.. Try another one'}, status=status.HTTP_400_BAD_REQUEST)
        if Advocate.objects.filter(enrollment_id = enrollment_id, is_verified = True).exists():
            return Response({'message' : 'This user alredy exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = UserData.objects.create_user(email=email, password=password, name=name)

        data = request.data.copy()
        data['user_id'] = user.id
        data['type_of_user'] = 'normal_advocate'

        serializer = NormalAdvocateSerializer(data=data, context = {'request' : request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"message": "validation failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class SuspendAdvocateView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin | IsAuthenticatedAssociationAdmin | IsAuthenticatedLawfirmAdmin]

    def patch(self, request, id):
        try :
            advocate = Advocate.objects.get(id = id)
            serializer=NormalAdvocateSerializer(advocate, context = {'request' : request})
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
            serializer = NormalAdvocateSerializer(advocate, data=request.data,partial=True, context = {'request' : request})
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
            serializer=NormalAdvocateSerializer(advocate, context = {'request' : request})
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
        serializer = NormalAdvocateSerializer(advocate, context = {'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# New views 

# membership status for advocate profile to know pending or approvied by anyone
class AdvocateAssociationMembershipStatus(APIView):
    # permission_classes = []

    def get(self, request):
        authenticated_adv = request.user
        advocate = AdvocateAssociation.objects.filter(advocate__user = authenticated_adv)
        serializer = AdvocateAssociationSerializer(advocate, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#View to display the expiry date of the advocate and also the how many days to the expiry date in advocate profile
class AdvocateCurrentMembershipExpiry(APIView):
    def get(self, request, ):
        authenticated_adv = request.user
        adv_associations = AssociationMembershipPayment.objects.filter(for_user_details__user = authenticated_adv, is_current = True)
        serializer = AssociationMembershipPaymentSerializer(adv_associations, many = True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

#Dipaly the advocates owned lawfirm
class AdvocateOwnLawfirm(APIView):
    def get(self, request):
       authenticated_adv= request.user
       advocateslawfirm = AdvocateLawfirm.objects.filter(advocate__user = authenticated_adv, is_owner = True)
       serializer = AdvocateLawfirmSerializer(advocateslawfirm, many = True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    

# to check the entollment id when the first time the user comes
class FirstLoginEnrollmentIdChecking(APIView):
    def post(self, request):
        enrol_id = request.data.get('enrollment_id')
        if RawData.objects.filter(enrollment_id = enrol_id).exists():
            return Response({'message' : 'User found with this entrollment id'},status=status.HTTP_200_OK)
        return Response({'message' : 'User not found with this entrollment id'},status=status.HTTP_200_OK)
    

class FirstLoginDetailsSubmmit(APIView):
    def post(self, request,enro_id):
        
        email = request.data.get('email')
        password = request.data.get('password')
        phone = request.data.get('phone')
        if UserData.objects.filter(email = email).exists():
            return Response({'message' : 'Email alredy exists.. Try another one'}, status=status.HTTP_400_BAD_REQUEST)
        if Advocate.objects.filter(enrollment_id =enro_id, is_verified = True).exists():
            return Response({'message' : 'This Enrollment ID alredy exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Advocate.objects.filter(phone = phone).exists():
            return Response({'message' : 'This Phone number alredy exists'}, status=status.HTTP_400_BAD_REQUEST)

        try :
            rawdata = RawData.objects.get(enrollment_id = enro_id)
        except RawData.DoesNotExist:
            return Response({'message' : 'Enrollment id cound not be found.. Please check your id'})
        name = rawdata.name
        user = UserData.objects.create(email = email, name = name,password =password)
        
        data = request.data.copy()
        data['user_id'] = user.id
        data['type_of_user'] = 'normal_advocate'
        data['enrollment_id'] = rawdata.enrollment_id
        serializer = NormalAdvocateSerializer(data=data, context = {'request' : request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "successfully created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"message": "validation failed", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)








