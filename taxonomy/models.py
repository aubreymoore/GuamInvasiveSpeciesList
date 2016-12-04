from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Taxon(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    rank = models.CharField(max_length=50)
    # timestamp = models.DateTimeField(null=True, blank=True)
    # created_by = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return self.name

    # def save(self):
    #     self.timestamp = timezone.now()
    #     super(Location, self).save()

    class MPTTMeta:
        order_insertion_by = ['name']
