from django.contrib import admin
from django.urls import path, include

from .views import (LawFirmListView,LawfirmEditFormView, LawfirmNotificationView, SuspendLawFirmView,EditLawfirmView, DeletelawFirmView,
                     LawfirmCountView, LawFirmAdvocateListView,LawfirmNotificationGetView, DeleteLawFirmAdvocateView,LawfirmInvitationRequestView, CreateLawFirmView)


urlpatterns = [
   path("list", LawFirmListView.as_view(), name = "LawFirmListView"),
   path("suspend-lawfirm/<id>", SuspendLawFirmView.as_view(),  name= "SuspendLawFirmView"),
   path("delete-lawfirm/<id>", DeletelawFirmView.as_view(),  name= "DeletelawFirmView"),
   path("edit-lawfirm/<id>", EditLawfirmView.as_view(),  name= "EditLawfirmView"),
   path("editform-lawfirm/<id>", LawfirmEditFormView.as_view(),  name= "LawfirmEditFormView"),
   path("create-lawfirm/<user_id>", CreateLawFirmView.as_view(), name = "CreateLawFirmView"),   #not in api
   path("count", LawfirmCountView.as_view(),  name= "LawfirmCountView"),

   path("list/<advocate_id>", LawFirmAdvocateListView.as_view(),  name= "LawFirmAdvocateListView"),
   path("delete/<advocate_id>", DeleteLawFirmAdvocateView.as_view(),  name= "DeleteAdvocateLawFirmView"),


   #new
   path("invite-advocate/<adv_id>", LawfirmInvitationRequestView.as_view(),  name= "LawfirmInvitationRequestView"),

   path("notification/list/<id>",LawfirmNotificationGetView.as_view() ,name="LawfirmNotificationGetView"),
   path("notification/edit/<id>",LawfirmNotificationView.as_view() ,name="LawfirmNotificationView"),
   path("notification/create/<id>",LawfirmNotificationView.as_view() ,name="LawfirmNotificationView"),
   path("notification/delete/<id>",LawfirmNotificationView.as_view() ,name="LawfirmNotificationView"),
]


