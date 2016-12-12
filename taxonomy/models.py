from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone

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
