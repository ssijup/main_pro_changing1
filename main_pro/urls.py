
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('impersonate/', include('impersonate.urls')),
    path('admin/', admin.site.urls),
    path('userapp/', include('userapp.urls')),
    path('advocates/', include('advocates.urls')),
    path('lawfirm/', include('lawfirm.urls')),
    path('registrar/', include('registrar.urls')),
    path('association/', include('association.urls')),
    path('netmagics/', include('netmagics.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
