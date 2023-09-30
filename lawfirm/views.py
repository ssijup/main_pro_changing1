from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.shortcuts import render
from rest_framework import status
from userapp.models import Advocate
from .models import LawfirmAdmin

from association.permissions import IsAuthenticatedNetmagicsAdmin
from .permissions import IsAuthenticatedLawfirmAdmin
from .serializer import LawFirmListSerializer, AdvocateLawfirmSerializer, LawFirmNotificationSerilaizer
from .models import LawFirm, AdvocateLawfirm, LawfirmNotification




class LawFirmListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        lawfirm = LawFirm.objects.all()
        serializer = LawFirmListSerializer(lawfirm, many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    
     
#creating a lawfirm and making the created user as the admin and owner of the lawfirm
class CreateLawFirmView(APIView):
    def post(self, request):
        auth_adv = request.user
        data = request.data
        try :
            advocate = Advocate.objects.get(user =  auth_adv)
            data['created_by']= advocate.id
            # advocate = Advocate.objects.get(id = user_id)
        except Advocate.DoesNotExist:
             return Response({'message' : 'Advocate could not be found at this moment... Please try after sometime'})
        serializer = LawFirmListSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                lawfirm=serializer.save()
                AdvocateLawfirm.objects.create(advocate=advocate,lawfirm =lawfirm, invitation_status = True, is_admin = True, is_owner = True )
                return Response({"message": "Lawfirm details created successfully"}, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:  
            return Response({
                "message": "Validation failed"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": "An unexpected error occurred",
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#creating lawfirm admin by the lawfirm owner only
class CreateLawfirmAdmin(APIView):
    # permission_classes = [isOwner]

    def post(self, request, adv_id,lawfirm_id):
        try :
            advocate = Advocate.objects.get(id =adv_id)
            lawfirm = LawFirm.objects.get(id = lawfirm_id)
            admin = AdvocateLawfirm.objects.get(advocate = advocate, lawfirm = lawfirm)
            admin.is_admin = True
            admin.save()
            return Response({'message' : 'Successfully made him as the admin'})
        except Advocate.DoesNotExist:
            return Response({"message" : "Advocate could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except LawFirm.DoesNotExist:
            return Response({"message" : "Lawfirm could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except AdvocateLawfirm.DoesNotExist:
            return Response({"message" : "Unable to find the user at this moment ... Please try after sometime"},status=status.HTTP_400_BAD_REQUEST)
        

        
          
class SuspendLawFirmView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def patch(self, request, id):
        try :
            lawfirm = LawFirm.objects.get(id = id)
            serializer=LawFirmListSerializer(lawfirm)
            lawfirm.is_suspend = not lawfirm.is_suspend
            lawfirm.save()

            if lawfirm.is_suspend:
                return Response({"message" : "LawFirm suspended sucessfully",  "data":serializer.data}, status = status.HTTP_202_ACCEPTED)
            return Response({"message" : "LawFirm suspension removed sucessfully", "data":serializer.data}, status = status.HTTP_202_ACCEPTED)

        except LawFirm.DoesNotExist:
            return Response({
                "message" : "LawFirm could not be found"
                }, status= status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeletelawFirmView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin]

    def delete(self, request, id):
        try:
            lawfirm=LawFirm.objects.get(id=id)
            lawfirm.delete()
            return Response({"message" : "LawFirm deleted sucessfully"})
        
        except LawFirm.DoesNotExist:
            return Response({"message" : "The LawFirm cout not be found"})
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditLawfirmView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin | IsAuthenticatedLawfirmAdmin]

    def patch(self, request, id):
        try:
            lawfirm=LawFirm.objects.get(id=id)
            serializer = LawFirmListSerializer(lawfirm, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "Lawfirm details updated sucessfully"},status=status.HTTP_200_OK)
            return Response({"message" : "Lawfirm could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except LawFirm.DoesNotExist:
            return Response({"message" : "Lawfirm could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message" : "An unexcepted error occured "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class LawfirmEditFormView(APIView):
    def get(self, request, id) :
        try:
            notification=LawFirm.objects.get(id=id)
            serializer=LawFirmListSerializer(notification)
            return Response(serializer.data ,status=status.HTTP_200_OK)

        except LawFirm.DoesNotExist:
                    return Response({"message" : "Lawfirm could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                    return Response({
                        "message": "An unexpected error occurred"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LawfirmCountView(APIView):
    def get(self, request):
        lawfirm_count = LawFirm.objects.count()
        return Response({'lawfirm_count': lawfirm_count}, status=status.HTTP_200_OK)
    

class LawFirmAdvocateListView(APIView):
    def get(self, request, id):
        advocate = AdvocateLawfirm.objects.filter(advocate__id=id)
        serializer = AdvocateLawfirmSerializer(advocate, many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)
    
class DeleteLawFirmAdvocateView(APIView):
    def delete(self, request, id):
        try:
            lawfirm=AdvocateLawfirm.objects.get(id=id)
            lawfirm.delete()
            return Response({"message" : "LawFirm deleted sucessfully"})
        
        except AdvocateLawfirm.DoesNotExist:
            return Response({"message" : "The LawFirm cout not be found"})
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Sending invitaion to advocate to join the lawfirm
class LawfirmInvitationRequestView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, adv_id, lawfirm_id):
        lawfirmadmin = request.user
        try :
            lawfirm = LawFirm.objects.get(id = lawfirm_id)
            # law_adv = AdvocateLawfirm.objects.get(advocate__user = lawfirmadmin, lawfirm = lawfirm)
            # admin_obj = LawfirmAdmin.objects.get(user = lawfirmadmin)
            # lawfirm = admin_obj.lawfirm
            advocate = Advocate.objects.get(id = adv_id)
            # inviation = AdvocateLawfirm.objects.get(advocate = advocate, lawfirm = lawfirm)
            AdvocateLawfirm.objects.create(advocate = advocate, lawfirm = lawfirm)
            return Response({'message' : ' Invitation Request send sucessfully'}, status=status.HTTP_201_CREATED)
        except LawFirm.DoesNotExist:
            return Response({'message' : 'Lawfirm could not be found at this moment... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        except Advocate.DoesNotExist:
            return Response({'message' : 'Advocate could not be found at this moment... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        except AdvocateLawfirm.DoesNotExist:
                return Response({'message' : 'An error  occured at this moment... Try again later'} , status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message' : 'An unexcepted  error occur'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#Advocate accepting the invitation from lawfirm
class LawfirmAcceptInvitationByAdvocate(APIView):
    def patch(self ,request, adv_id, lawfirm_id):
        try :
            lawfirm = LawFirm.objects.get(id = lawfirm_id)
            advocate = Advocate.objects.get(id = adv_id)
            advocateinvitation = AdvocateLawfirm.objects.get(advocate =advocate ,lawfirm = lawfirm)
            if advocateinvitation.invitation_status == False :
                advocateinvitation.invitation_status = True
                advocateinvitation.save()
                return Response({'message' : 'You accepted the request and is now a member of that lawfirm'}, status = status.HTTP_202_ACCEPTED)
            return Response({'message' : 'You accepted the request and is now a member of that lawfirm'}, status = status.HTTP_202_ACCEPTED)

        except LawFirm.DoesNotExist:
            return Response({'message' : 'Lawfirm could not be found at this moment... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        except Advocate.DoesNotExist:
            return Response({'message' : 'Advocate could not be found at this moment... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        except AdvocateLawfirm.DoesNotExist:
            return Response({'message' : 'Invitation cound not be send at this time... Try agin later'} , status=status.HTTP_404_NOT_FOUND)


#Displaying the invitaion from lawfirm in advocate profile 
class LawfirmInvitaionInAdvocateProfile(APIView):
    def get(self, request):
        authenticated_adv = request.user
        lawfirm_invitaion = AdvocateLawfirm.objects.filter(advocate__user = authenticated_adv).exclude(invitation_status = True)
        serializer = AdvocateLawfirmSerializer(lawfirm_invitaion, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
         

# to display the selected invitaion details in the  advocate profile
class LawfirmSelectedInvitaionInAdvocateProfile(APIView):
    def get(self, request,inv_id):
        try:
            invitation = AdvocateLawfirm.objects.get(id = inv_id)
        except AdvocateLawfirm.DoesNotExist:
            return Response({'message' : 'Invitation details cound not be found at this time... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        serializer = AdvocateLawfirmSerializer(invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)



#Displaying the invitation status ,admin,owner  request in Lawfirm admin dashboard
class LawfirmRelatedGetView(APIView):
    def get(self , request,lawfirm_id):
        admin = request.user
        try:
            lawfirm = LawFirm.objects.get(id = lawfirm_id)
            adv_lawfirm = AdvocateLawfirm.objects.get(advocate__user = admin, lawfirm= lawfirm)
        except LawFirm.DoesNotExist:
            return Response({'message' : 'lawfirm could not be found at this moment... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        except AdvocateLawfirm.DoesNotExist:
            return Response({'message' : 'The advocate associated to the lawfirm could not be found at this moment... Try agin later'} , status=status.HTTP_404_NOT_FOUND)
        serializer = AdvocateLawfirmSerializer(adv_lawfirm)
        return Response(serializer.data , status=status.HTTP_200_OK)



class LawfirmNotificationGetView(APIView):
    # permission_classes = [IsAuthenticated]LawfirmNotification

    def get(self, request, id):
        notification=LawfirmNotification.objects.filter(lawfirm__id = id)
        serializer=LawFirmNotificationSerilaizer(notification,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class LawfirmNotificationView(APIView):
    # permission_classes = [IsAuthenticatedNetmagicsAdmin | IsAuthenticatedAssociationAdmin]

    def post(self, request, id ):
        data=request.data
        try:
            lawfirm=LawFirm.objects.get(id=id)
            serializer=LawFirmNotificationSerilaizer(data=data)
            if serializer.is_valid():
                serializer.validated_data['lawfirm']=lawfirm
                serializer.save()
                # notification=Notification(association=association)
                # notification.save()
                return Response({"message":"Notification content created successfully"})
            return Response({"message" : "Something went wrong"},status=status.HTTP_400_BAD_REQUEST)                                
        except LawFirm.DoesNotExist:
            return Response({"message":"Lawfirm could not be found"})
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred "
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
    def patch(self, request, id):
        try:
            notification=LawfirmNotification.objects.get(id=id)
            data=request.data
            serializer=LawFirmNotificationSerilaizer(notification,data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Notification updated successfully"})
            return Response({"message" : "Something went wrong"},status=status.HTTP_400_BAD_REQUEST)                         
        except LawfirmNotification.DoesNotExist:
                    return Response({"message" : "Notification content could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                    return Response({
                        "message": "An unexpected error occurred "
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, id):
        try:
            notification = LawfirmNotification.objects.get(id=id)
            notification.delete()
            return Response({"message": "Notification deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except LawfirmNotification.DoesNotExist:
            return Response({"message": "Notification content could not be found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An unexpected error occurred: "},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


#Suspendin advocates in Lawfirm
class SuspendLawfirmAdvocates(APIView):
    def patch(self , request, suspend_adv_id,lawfirm_id):
        try :
            advocate = Advocate.objects.get(id =suspend_adv_id)
            lawfirm = LawFirm.objects.get(id = lawfirm_id)
            suspend_related = AdvocateLawfirm.objects.get(advocate = advocate, lawfirm = lawfirm)
            suspend_related.advocate_status = False
            suspend_related.save()
            return Response({'message' : 'Advocate suspended sucessfully'}, status= status.HTTP_200_OK)
        except Advocate.DoesNotExist:
            return Response({"message" : "Advocate could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except LawFirm.DoesNotExist:
            return Response({"message" : "Lawfirm could not be found"},status=status.HTTP_400_BAD_REQUEST)
        except AdvocateLawfirm.DoesNotExist:
            return Response({"message" : "Unable to find the user at this moment ... Please try after sometime"},status=status.HTTP_400_BAD_REQUEST)
        


# Withdrawing the invitaion for an advocate to join the Lawfirm
class WithdrawInvitaionByLawfirm(APIView):
    def patch(self , request,lawfirm_id, adv_id):
        
        # withdraw_invitation = AdvocateLawfirm.objects.get(advocate__id = adv_id, lawfirm__id = lawfirm_id)
        invitation = get_object_or_404(AdvocateLawfirm, advocate__id=adv_id, lawfirm__id=lawfirm_id)
        invitation.delete()
        return Response({'message' : 'Invitation withdrawed sucessfull'}, status= status.HTTP_200_OK)




