from django.contrib import admin
from django.urls import path, include

from .views import (FirstLoginEnrollmentIdChecking, FirstLoginDetailsSubmmit,AdvocateOwnLawfirm, AdvocatesListView, SuspendAdvocateView, EditAdvocateProfileView,
                    CreateAdvocatesListView,AdvocateEditFormView,AdvocatesPaymentView, AssociationAdvocateView,
                     AdvocateLawFirmListView, DeleteAdvocateLawFirmView, AssociationAdvocateViewUsingID,
                      AdvocateMembershipsView,AdvocateAssociationMembershipStatus, AdvocateMembershipsViewUsingID,
                       AdvocateCurrentMembershipExpiry, AdvocatesProfileView )

urlpatterns = [
   path("list", AdvocatesListView.as_view(), name = "AdvocatesListView"),
   path("create-advocate", CreateAdvocatesListView.as_view(), name = "CreateAdvocatesListView"),
   path("suspend-advocate/<id>", SuspendAdvocateView.as_view(), name = "SuspendAssociationView"),
   path("edit-advocate/<id>", EditAdvocateProfileView.as_view(), name = "EditAdvocateProfileView"),
   path("editform-advocate/<id>", AdvocateEditFormView.as_view(), name = "AdvocateEditFormView"),
   path("payments/<id>", AdvocatesPaymentView.as_view(), name = "AdvocatesPaymentView"),

   # path("list/<id>", AssociationAdvocateView.as_view(), name = "AssociationAdvocateView"),

   path("list-advocates/<id>", AdvocateLawFirmListView.as_view(), name = "AdvocateLawFirmListView"),
   path("delete-advocates/<lawfirm_id>", DeleteAdvocateLawFirmView.as_view(), name = "DeleteAdvocateLawFirmView"),

   path("association/list/<id>", AssociationAdvocateViewUsingID.as_view(), name = "AssociationAdvocateViewUsingID"),#changed
   path("association/list", AssociationAdvocateView.as_view(), name = "AssociationAdvocateView"),#changed

   path("list-advocates/<lawfirm_id>", AdvocateLawFirmListView.as_view(), name = "AdvocateLawFirmListView"),
   path("delete-advocates/<lawfirm_id>", DeleteAdvocateLawFirmView.as_view(), name = "DeleteAdvocateLawFirmView"),

   path("membership/list", AdvocateMembershipsView.as_view(), name = "AssociationMembershipView"),
   path("membership/list/<id>", AdvocateMembershipsViewUsingID.as_view(), name = "AssociationMembershipViewUsingID"),   

   path("profile", AdvocatesProfileView.as_view(), name = "AdvocatesProfileView"),





# membership status for advocate profile to know pending or approvied by anyone
   path("membership-status", AdvocateAssociationMembershipStatus.as_view(), name = "AdvocateAssociationMembershipStatus"),
   path("membership-expiry", AdvocateCurrentMembershipExpiry.as_view() ,name="AdvocateCurrentMembershipExpiry"),



#Lising advocate owned lawfirm
   path("own-lawfirm", AdvocateOwnLawfirm.as_view() ,name="AdvocateOwnLawfirm"),

#NEW

# POST -to check the entrollment id while first login
   path("id-verification", FirstLoginEnrollmentIdChecking.as_view() ,name="FirstLoginEnrollmentIdChecking"),

#first login details submmiting
   path("login-details-submmit/<enro_id>", FirstLoginDetailsSubmmit.as_view() ,name="FirstLoginDetailsSubmmit"),


]

# {
# "name" : "sonu",
# "password" : "sonu",
# "email" : "sonu@gmail.com",

# }