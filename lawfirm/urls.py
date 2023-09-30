from django.contrib import admin
from django.urls import path, include

from .views import (LawfirmSelectedInvitaionInAdvocateProfile, WithdrawInvitaionByLawfirm, LawfirmRelatedGetView, SuspendLawfirmAdvocates, CreateLawfirmAdmin,LawFirmListView,LawfirmEditFormView, LawfirmNotificationView, SuspendLawFirmView,EditLawfirmView, DeletelawFirmView,
                     LawfirmCountView, LawFirmAdvocateListView,LawfirmNotificationGetView,LawfirmAcceptInvitationByAdvocate, LawfirmInvitaionInAdvocateProfile,DeleteLawFirmAdvocateView,LawfirmInvitationRequestView, CreateLawFirmView)


urlpatterns = [
   path("list", LawFirmListView.as_view(), name = "LawFirmListView"),
   path("suspend-lawfirm/<id>", SuspendLawFirmView.as_view(),name= "SuspendLawFirmView"),
   path("delete-lawfirm/<id>", DeletelawFirmView.as_view(),name= "DeletelawFirmView"),
   path("edit-lawfirm/<id>", EditLawfirmView.as_view(),name= "EditLawfirmView"),
   path("editform-lawfirm/<id>", LawfirmEditFormView.as_view(),name= "LawfirmEditFormView"),
   path("create-lawfirm", CreateLawFirmView.as_view(), name = "CreateLawFirmView"),   #not in api
   path("count", LawfirmCountView.as_view(),name= "LawfirmCountView"),

   path("list/<advocate_id>", LawFirmAdvocateListView.as_view(),name= "LawFirmAdvocateListView"),
   path("delete/<advocate_id>", DeleteLawFirmAdvocateView.as_view(),name= "DeleteAdvocateLawFirmView"),


   #new

   #invitations
   path("invite-advocate/<adv_id>/<lawfirm_id>", LawfirmInvitationRequestView.as_view(),name= "LawfirmInvitationRequestView"),
   path("invitation-in-advocate", LawfirmInvitaionInAdvocateProfile.as_view(),name= "LawfirmInvitaionInAdvocateProfile"),
   path("accept-invitation-advocate/<adv_id>/<lawfirm_id>", LawfirmAcceptInvitationByAdvocate.as_view(),name= "LawfirmAcceptInvitationByAdvocate"),
   path("invitation-details/<inv_id>", LawfirmSelectedInvitaionInAdvocateProfile.as_view(),name= "LawfirmSelectedInvitaionInAdvocateProfile"),


   #notifications
   path("notification/list/<id>",LawfirmNotificationGetView.as_view() ,name="LawfirmNotificationGetView"),
   path("notification/edit/<id>",LawfirmNotificationView.as_view() ,name="LawfirmNotificationView"),
   path("notification/create/<id>",LawfirmNotificationView.as_view() ,name="LawfirmNotificationView"),
   path("notification/delete/<id>",LawfirmNotificationView.as_view() ,name="LawfirmNotificationView"),



   path("create-admin/<adv_id>/<lawfirm_id>",CreateLawfirmAdmin.as_view() ,name="CreateLawfirmAdmin"),
   path("suspend-advocate/<suspend_adv_id>/<lawfirm_id>",SuspendLawfirmAdvocates.as_view() ,name="SuspendLawfirmAdvocates"),
   path("related-views/<lawfirm_id>",LawfirmRelatedGetView.as_view() ,name="LawfirmRelatedGetView"),
   path("withdraw-invitation/<lawfirm_id>/<adv_id>",WithdrawInvitaionByLawfirm.as_view() ,name="WithdrawInvitaionByLawfirm"),



   
]




