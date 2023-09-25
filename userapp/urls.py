from django.urls import path
from .views import (CustomTokenObtainPairSerializer,CustomTokenObtainPairView, AdvocatePasswordChangeView,
                    AdvocatesCountView, TestapiForAuthr, TypeOfUserGetView, ForgotPasswordEmailRequest,
                     ForgotPasswordEmailConfirmation )
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    # path('api/login/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('advocates/change-password/<id>', AdvocatePasswordChangeView.as_view(), name='change-password'),
    path('advocates/count', AdvocatesCountView.as_view(),name='AdvocatesCountView'),

    path('forgot-password-email/request',ForgotPasswordEmailRequest.as_view(),name='ForgotPasswordEmailRequest'),
    path('forgot-password-email/confirm',ForgotPasswordEmailConfirmation.as_view(),name='ForgotPasswordEmailConfirmation'),

    path('test_api_for_authr',TestapiForAuthr.as_view(),name='TestapiForAuthr'),
    path('type-of-user',TypeOfUserGetView.as_view(),name='TypeOfUserGetView'),


]
