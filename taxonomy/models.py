from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
import uuid
from publications import models as pub_models
from django.contrib import admin

class NameFinderJSON(models.Model):
    pub = models.ForeignKey(pub_models.Publication)
    name_finder_json = models.TextField()

class NameFinderResult(models.Model):
    pub = models.ForeignKey(pub_models.Publication)

    verified = models.NullBooleanField()

    is_known_name = models.BooleanField()
    supplied_name_string = models.CharField(max_length=255, blank=True)

    classification_path_ranks = models.CharField(max_length=255, blank=True)
    classification_path = models.CharField(max_length=255, blank=True)
    current_name_string = models.CharField(max_length=255, blank=True)
    imported_at = models.CharField(max_length=255, blank=True)
    canonical_form = models.CharField(max_length=255, blank=True)
    data_source_id = models.IntegerField(null=True)
    match_value = models.CharField(max_length=255, blank=True)
    data_source_title = models.CharField(max_length=255, blank=True)
    gni_uuid = models.CharField(max_length=255, blank=True)
    edit_distance = models.IntegerField(null=True)
    match_type = models.IntegerField(null=True)
    name_string = models.CharField(max_length=255, blank=True)
    current_taxon_id = models.CharField(max_length=255, blank=True)
    taxon_id = models.CharField(max_length=255, blank=True)
    prescore = models.CharField(max_length=255, blank=True)
    classification_path_ids = models.CharField(max_length=255, blank=True)
    score = models.FloatField(null=True)

    def __str__(self):
        return self.classification_path



class RawName(models.Model):
    name = models.CharField(max_length=50)
    pub = models.ForeignKey(pub_models.Publication)

    def __str__(self):
        return self.name

class RawNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub')





class Taxon(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    rank = models.CharField(max_length=50)
    created = models.DateTimeField(editable=False)
    created_by = models.CharField(max_length=50,null=True, blank=True)
    modified = models.DateTimeField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Taxon, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

class DwcaTaxon(models.Model):
    uuid = models.UUIDField(primary_key=True)
    scientificName = models.CharField(max_length=50,null=False, blank=False)
    taxonRank = models.CharField(max_length=50,null=False, blank=False)
    kingdom = models.CharField(max_length=50,null=False, blank=False)
    bibliographicCitation = models.CharField(max_length=50,null=False, blank=False)

    def __str__(self):
        return self.scientificName


class DwcaDistribution(models.Model):
    uuid = models.ForeignKey(DwcaTaxon, on_delete=models.CASCADE)
    locality = models.CharField(max_length=50,null=False, blank=False)
    occurrenceRemarks = models.CharField(max_length=50,null=False, blank=False)

class DwcaVernacular(models.Model):
    uuid = models.ForeignKey(DwcaTaxon, on_delete=models.CASCADE)
    vernacularName = models.CharField(max_length=50,null=False, blank=False)

class DwcaResourceRelationship(models.Model):
    uuid = models.ForeignKey(DwcaTaxon, on_delete=models.CASCADE)
    relationshipOfResource = models.CharField(max_length=50,null=False, blank=False)
    relatedResourceID = models.ForeignKey(DwcaTaxon, related_name='rrlink' )


"""
Darwin Core Archive file upload using Admin form
"""
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Restrict uploads to zip files.
def validate_file_extension(value):
    if not value.name.endswith('.zip'):
        raise ValidationError(u'Error message: Your Darwin Core Archive must be a zip file.')

# Model containing only a FileField
class Upload_dwca(models.Model):
    dwca = models.FileField(upload_to='dwca/', validators=[validate_file_extension])

# This code deletes files when associated records are deleted from the Upload_dwca DB table.
# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=Upload_dwca)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.dwca.delete(False)
