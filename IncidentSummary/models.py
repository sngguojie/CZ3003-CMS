from __future__ import unicode_literals

from django.db import models

# Create your models here.

class IncidentSummary(models.Model):
    datetime = models.DateField()
    description = models.TextField()
    
    def __unicode__(self):              # __unicode__ on Python 2
        return self.description