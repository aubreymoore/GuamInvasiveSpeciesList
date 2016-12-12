from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Taxon, Upload_dwca

admin.site.register(Taxon, MPTTModelAdmin)
admin.site.register(Upload_dwca)
