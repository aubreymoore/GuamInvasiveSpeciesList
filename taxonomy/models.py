from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Taxon(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    rank = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']
