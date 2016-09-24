from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IncidentSummary(models.Model):
    datetime = models.DateField()
    description = models.TextField()
    creator = models.ForeignKey(User)
    
    def __unicode__(self):              # __unicode__ on Python 2
        return self.description