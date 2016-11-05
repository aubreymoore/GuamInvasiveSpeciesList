from django.db import models
from django.utils.timezone import now

class NewIslandRecord(models.Model):
    taxon = models.ForeignKey('taxonomy.Taxon')
    location = models.ForeignKey('locations.Location')
    year_detected = models.IntegerField(null=True)
    reference = models.ForeignKey('publications.Publication', null=True)
    invasive_species = models.NullBooleanField()
    established = models.NullBooleanField()
    quarantine_interception = models.NullBooleanField()

    def __str__(self):
        return('{} {}'.format(self.taxon, self.year_detected))
