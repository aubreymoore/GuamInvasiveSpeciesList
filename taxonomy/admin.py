from __future__ import unicode_literals

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Taxon
from .models import Upload_dwca
from .models import DwcaTaxon
from .models import DwcaDistribution
from .models import DwcaResourceRelationship
from .models import DwcaVernacular
from .models import RawName
from .models import RawNameAdmin
from .models import NameFinderResult
from .models import NameFinderJSON
#from .models import NameFinderResultAdmin

from django.contrib.admin import AdminSite
from django.http import HttpResponse
import logging

'''
The following code extends the admin change form for Publication
(/publications/publication).

It adds a new action, "find_names".

Reference: https://docs.djangoproject.com/en/1.10/ref/contrib/admin/actions/
'''
from publications.admin import PublicationAdmin
from publications.models import Publication
from publications.models import CustomFile
import requests
import json
import time
from django.core.files.base import ContentFile
import json
from taxonomy.functions import json_to_db
from taxonomy.functions import find_names
from taxonomy.functions import json_to_name_finder_results

#Get an instance of a logger
logger = logging.getLogger(__name__)

class CustomPublicationAdmin(PublicationAdmin):
    actions = ['add_extracted_taxon_names_file']

    def add_extracted_taxon_names_file(self, request, queryset):
        for pub in queryset:
            print('title: {} url: {}'.format(pub.title, pub.url))
            file_list = CustomFile.objects.filter(
                publication_id=pub.id).filter(
                description='extracted taxon names')
            if not file_list:
                taxa = find_names(pub.url)
                json_string = json.dumps(taxa)
                django_file = ContentFile(json_string)
                newfile = CustomFile()
                newfile.publication_id = pub.id
                newfile.description = 'extracted taxon names'
                newfile.file.save('extracted_taxon_names.json', django_file, save=True)
                print('new file attached.')
                print('adding data to NameFinderResults model ...')
                json_to_name_finder_results(pub, taxa)
                json_to_db(pub, taxa)
                print('FINIS')
            else:
                print('A file with description "extracted_taxon_names" already exists')

    add_extracted_taxon_names_file.short_description = "Extract scientific names from selected publications"

admin.site.unregister(Publication)
admin.site.register(Publication, CustomPublicationAdmin)
'''
End of code section.
'''

# Add mark_as_verified action to NameFinderResultAdmin change page

def mark_as_verified(self, request, queryset):
    queryset.update(verified=True)
mark_as_verified.short_description = 'Mark selected results as verified'

# http://www.gbif.org/species/1406619


class NameFinderResultAdmin(admin.ModelAdmin):
    list_filter = ('pub', 'verified',)
    list_display = ('verified', 'classification_path', 'GBIF')
    list_display_links = ('classification_path',)
    readonly_fields = (
        'GBIF',
        'pub',
        'is_known_name',
        'supplied_name_string',
        'classification_path_ranks',
        'classification_path',
        'current_name_string',
        'imported_at',
        'canonical_form',
        'data_source_id',
        'match_value',
        'data_source_title',
        'gni_uuid',
        'edit_distance',
        'match_type',
        'name_string',
        'current_taxon_id',
        'taxon_id',
        'prescore',
        'classification_path_ids',
        'score',)
    actions = [mark_as_verified]

    def GBIF(self, obj):
        return '<a  target="_blank" href="http://www.gbif.org/species/{}">{}</a>'.format(obj.taxon_id, obj.taxon_id)
    GBIF.allow_tags = True



admin.site.register(NameFinderResult, NameFinderResultAdmin)



admin.site.register(Taxon, MPTTModelAdmin)
admin.site.register(Upload_dwca)
admin.site.register(DwcaTaxon)
admin.site.register(DwcaDistribution)
admin.site.register(DwcaResourceRelationship)
admin.site.register(DwcaVernacular)
admin.site.register(RawName, RawNameAdmin)
admin.site.register(NameFinderJSON)




# Ref for subclassing AdminSite:
# http://stackoverflow.com/questions/35875454/django-admin-extending-admin-with-custom-views
class MyAdminSite(AdminSite):

    def custom_view(self, request):
        return HttpResponse("Test")

    def get_urls(self):
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        urls += [
            url(r'^custom_view/$', self.admin_view(self.custom_view))
        ]
        return urls

admin_site = MyAdminSite()


# @admin.register(DwcaTaxon, site=admin_site)
# class SomeModelAdmin(admin.ModelAdmin):
#     pass
