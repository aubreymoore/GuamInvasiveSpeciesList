from django.db import models

class NewIslandRecord(models.Model):
    taxon = models.ForeignKey('taxonomy.Taxon')
    location = models.ForeignKey('locations.Location')
    year_detected = models.IntegerField(null=True)
    reference = models.ForeignKey('publications.Publication', null=True)
    invasive_species = models.NullBooleanField()
    established = models.NullBooleanField()
    quarantine_interception = models.NullBooleanField()

    # Metadata
    created = models.DateField(null=True)
    created_by = models.CharField(max_length=30, null=True)
    update_by = models.CharField(max_length=30, null=True, blank=True)
    updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return('{} {}'.format(self.taxon, self.year_detected))
