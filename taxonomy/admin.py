from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Taxon

admin.site.register(Taxon, MPTTModelAdmin)
