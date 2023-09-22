from django.contrib import admin
from .models import LawFirm,LawfirmAdmin, AdvocateLawfirm



admin.site.register(LawFirm)
admin.site.register(LawfirmAdmin)
admin.site.register(AdvocateLawfirm)