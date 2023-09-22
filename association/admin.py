from .models import ( Court,Jurisdiction,Association,AssociationMembershipPayment,AssociationPaymentRequest, 
                     Notification,MembershipFineAmount,MembershipPlan, AssociationSuperAdmin,AdvocateAssociation )
from django.contrib import admin

# Register your models here.

admin.site.register(Court)
admin.site.register(Jurisdiction)
admin.site.register(Association)
admin.site.register(AssociationMembershipPayment)
admin.site.register(AssociationPaymentRequest)
admin.site.register(Notification)
admin.site.register(MembershipFineAmount)
admin.site.register(MembershipPlan)
admin.site.register(AssociationSuperAdmin)
admin.site.register(AdvocateAssociation)

