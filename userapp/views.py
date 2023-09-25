from .serializers import CustomTokenObtainPairSerializer, PasswordChangeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from .serializers import CustomTokenObtainPairSerializer, EmailOtpRequestSerializer, EmailOtpConfirmSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserData, Advocate
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class AdvocatePasswordChangeView(APIView):
    def post(self, request, id):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # user = self.request.user
            try:
                advocate=Advocate.objects.get(id=id)
                user=advocate.user
                user=UserData.objects.get(id=id)
            except:
                 pass
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been changed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdvocatesCountView(APIView):
    def get(self, request):
        advocates_count = Advocate.objects.count()
        return Response({'advocates_count': advocates_count}, status=status.HTTP_200_OK)



class TestapiForAuthr(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user
        print("user :",user.name,"  ",user.id,"  ", user.email)
        auth_header = request.headers.get('Authorization')
        print("siju",auth_header)
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]

            decoded_payload = token_backend.decode(token)
            user_id = decoded_payload.get('user_id')
            # username = decoded_payload.get('username')
            email = decoded_payload.get('email')  # If email is included in the token payload
            print("email :", email ,user_id)
            return Response({"message" : "success"})

        else:
            return Response({"message" : "failed"})
        
class TypeOfUserGetView(APIView):     
    def get(self, request):
        user=request.user
        print("user :",user.name,"  ",user.id,"  ", user.email)
        # auth_header = request.headers.get('Authorization')
        print("related:",user.has_related_objects())
        if user.name:
            return Response(user.has_related_objects())
        else:
            return Response(user.has_related_objects())
        

from django.core.mail import send_mail
from django.conf import settings
import random

class ForgotPasswordEmailRequest(APIView):  
    def post(self, request):
        serializer = EmailOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            otp = random.randint(100001, 999999)
            print("OTP",otp)
            print(type(otp))
            email = serializer.validated_data['email']
            try:
                UserData.objects.filter(email=email).update(otp=otp)
            except:
                return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            subject = 'Email Verification OTP'
            message = f'Your OTP for email verification is: {otp}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return Response({'message': 'otp sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordEmailConfirmation(APIView):  
    def post(self, request):
        serializer = EmailOtpConfirmSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            user = UserData.objects.get(email=email,otp=otp)
            print(user)
            if user is not None:
                user.set_password(new_password)
                user.save()
                otp = random.randint(100001, 999999)
                UserData.objects.filter(email=email).update(otp=otp)
            else:
                return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)