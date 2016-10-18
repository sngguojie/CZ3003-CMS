from __future__ import unicode_literals

from django.db import models

# Create your models here.
class IncidentCallReport(models.Model):
	caller_name= models.TextField()
	caller_nric= models.CharField(max_length=9)
	contact_no=models.CharField(max_length=8)
	description= models.TextField()
	Incident_type=models.CharField(max_length=1)
	dateTime=models.DateField()

	def __unicode__(self):              # __unicode__ on Python 2
        	return self.description
