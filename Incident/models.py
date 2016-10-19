from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Incident(models.Model):
    activation_time = models.DateTimeField(null=True)
    deactivation_time = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    incident_type=models.CharField(null=True, blank=True, max_length=1)
    
    def __unicode__(self):              # __unicode__ on Python 2
        return self.description