from django.db import models

class NewIslandRecord(models.Model):
    taxon = models.ForeignKey('taxonomy.Taxon')
    location = models.ForeignKey('locations.Location')
