from django.urls import path
from .views import AcivityTrackerView

from django.urls import path, include

from .views import (LoginForParticularAssocitionUser, ArchivingActivityTracterOldData, StartImpersonatingByNetmagicsAdmin,
                    StopImpersonatingByNetmagicsAdmin, NetmagicsAdminCreateView, ListNetmagicsAdmin, DeleteNetmagicsAdmin)


urlpatterns = [
    #Registrar view
    path("admin/create", NetmagicsAdminCreateView.as_view(), name = "NetmagicsAdminCreateView"),  
    path("admin/list", ListNetmagicsAdmin.as_view(), name = "ListNetmagicsAdmin"),  
    path("admin/delete/<id>", DeleteNetmagicsAdmin.as_view(), name = "DeleteNetmagicsAdmin"),  
    path('activity-tracker/list', AcivityTrackerView.as_view(), name='ActivityTrackerSerializer'),

    path('admin/impersonate/start/<id>', StartImpersonatingByNetmagicsAdmin.as_view(), name='start_impersonation'),
    path('admin/impersonate/stop/<id>', StopImpersonatingByNetmagicsAdmin.as_view(), name='stop_impersonation'),

    path('archive-activitytrcker', ArchivingActivityTracterOldData.as_view(), name='ArchivingActivityTracterOldData'),

    #NEW
    path('auth-user', LoginForParticularAssocitionUser.as_view(), name='LoginForParticularAssocitionUser'),

    

    
]




