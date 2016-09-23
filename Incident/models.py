from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Incident(models.Model):
    activation_date = models.DateField()
    deactivation_date = models.DateField()
    description = models.TextField()
    incident_summary = models.ForeignKey(IncidentSummary, on_delete=models.CASCADE)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.description