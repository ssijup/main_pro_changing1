from django.contrib import admin
from django.urls import path, include

from .views import (CourtSortedListView,AssociationListView,CourtListView, SuspendAssociationView,NotificationGetView,
                    EditCourtView,MembershipGetView,MembershipPlanView,EditAssociationView,CourtEditFormView,
                    ToggleMembershipFineAmountView,Paymentsucessfull,ToggleMembershipPlanView, AssociationEditFormView,
                    MembershipPaymentView,DeleteAssociationView, NotificationView, NotificationEditFormView,
                    NormalAdminView, DeleteAssociationView, CreateCourtView, CreateNormalAdminView, 
                    DeleteNormalAdminView,MembershipFineGetView,SuperAdminView, CreateSuperAdminView,DeleteSuperAdminView, 
                     CourtCountView, AssociationCountView, AssociationPaymentView, MembershipApprovalView,AssociationAdvocatesView,
                     MembershipPaymentListView, CreateAssociationView, AdvocatesViewUsingID,
                     MembershipGetViewUsingAssociationID, AdvocateMembershipRequestInAssociation)


urlpatterns = [
    
#court
   path("court/list", CourtListView.as_view(), name = "CourtListView"),
   path("court/create-court", CreateCourtView.as_view(), name = "CreateCourtView"),
   path("court/edit-court/<id>", EditCourtView.as_view(), name = "EditCourtView"),
   path("court/delete-court/<id>", CourtListView.as_view(), name = "CourtListView"),
   path("court/editform-court/<id>", CourtEditFormView.as_view(), name = "CourtEditFormView"),
   path("court/count/",CourtCountView.as_view(), name="CourtCountView"),


#association
   path("list", AssociationListView.as_view(), name = "AssociationListView"),
   path("create-association/<id>", CreateAssociationView.as_view(), name = "CreateAssociationView"),
   path("edit-association/<id>", EditAssociationView.as_view(), name = "EditAssociationView"),
   path('delete-association/<id>',DeleteAssociationView.as_view(),name="DeleteAssociationView"),
   path("editform-association/<id>",AssociationEditFormView.as_view() ,name="AssociationEditFormView"),
   path("suspend-association/<id>", SuspendAssociationView.as_view(), name = "SuspendAssociationView"),
   path("count", AssociationCountView.as_view(),  name= "AssociationCountView"),

 #admins  
   path("association-normal-admin/list",NormalAdminView.as_view() ,name="NormalAdminView"),
   path("association-normal-admin/create/<id>",CreateNormalAdminView.as_view() ,name="CreateNormalAdminView"),
   path("association-normal-admin/delete/<id>",DeleteNormalAdminView.as_view() ,name="DeleteNormalAdminView"),
   path("association-super-admin/list",SuperAdminView.as_view() ,name="SuperAdminView"), #made changes
   path("association-super-admin/create/<id>",CreateSuperAdminView.as_view() ,name="CreateSuperAdminView"),
   path("association-super-admin/delete/<id>",DeleteSuperAdminView.as_view() ,name="DeleteSuperAdminView"),



#membership plan
   path("membership-plan/list",MembershipGetView.as_view(),name="MembershipGetView"),#made changes
   path("membership-plan/list/<id>",MembershipGetViewUsingAssociationID.as_view(),name="MembershipGetViewUsingAssociationID"),

   path("membership-plan/create",MembershipPlanView.as_view(),name="MembershipPlanView"),
   path("membership-plan/edit/<id>",ToggleMembershipPlanView.as_view(),name="ToggleMembershipPlanView"),
   path("membership-plan/delete/<id>",ToggleMembershipPlanView.as_view(),name="ToggleMembershipPlanView"),
   path("membership-plan/editform/<id>",ToggleMembershipPlanView.as_view(),name="ToggleMembershipPlanView"),


#membership fine amount
   path("fine-amount/create/<id>",ToggleMembershipFineAmountView.as_view(),name="ToggleMembershipFineAmountView"),
   path("fine-amount/edit/<id>",ToggleMembershipFineAmountView.as_view(),name="ToggleMembershipFineAmountView"),
   path("fine-amount/delete/<id>",ToggleMembershipFineAmountView.as_view(),name="ToggleMembershipFineAmountView"),
   path("fine-amount/list/<id>",MembershipFineGetView.as_view(),name="ToggleMembershipFineAmountView"),  


#payment
   path('Paymentsucessfull/', Paymentsucessfull.as_view(), name='paymentsucessfull'),
   path("membership-payment/create/<user_id>/<plan_id>/<association_id>",MembershipPaymentView.as_view() ,name="MembershipPaymentView"),
   path("membership-payment/list",MembershipPaymentListView.as_view() ,name="MembershipPaymentListView"),


 #notification
   path("notification/list/<id>",NotificationGetView.as_view() ,name="NotificationGetView"),
   path("notification/edit/<id>",NotificationView.as_view() ,name="NotificationView"),
   path("notification/create/<id>",NotificationView.as_view() ,name="NotificationView"),
   path("notification/delete/<id>",NotificationView.as_view() ,name="NotificationView"),
   path("editform-notification/<id>",NotificationEditFormView.as_view() ,name="NotificationEditFormView"),

   path("payments/<association_id>",AssociationPaymentView.as_view() ,name="AssociationPaymentView"),

   # AssociationAdvocatesView
   path("list/<id>",AssociationAdvocatesView.as_view() ,name="AssociationAdvocatesView"),

   # AssociationAdvocatesView
   path("advocates/list", AssociationAdvocatesView.as_view() ,name="AssociationAdvocatesView"),
   path("advocates/list/<id>", AdvocatesViewUsingID.as_view() ,name="AdvocatesViewUsingID"),


# Advocate Membership approving by assocition admin or registrar view
   path("advocates/membership-approval/<id>", MembershipApprovalView.as_view() ,name="MembershipApprovalView"),

# To avoid listing of courts alredy assigned to a Registrar
   path("court/sorted/list", CourtSortedListView.as_view() ,name="CourtSortedListView"),

# to display Advocate membership rtequest in association admin dashboard
   path("advocate/membership-request-list", AdvocateMembershipRequestInAssociation.as_view() ,name="AdvocateMembershipRequestInAssociation"),


]