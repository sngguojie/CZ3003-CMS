from __future__ import unicode_literals

from django.db import models

# Create your models here.
class IncidentCallReport(models.Model):
	caller_name= models.TextField()
	contact_no=models.CharField(max_length=8)
	description= models.TextField()
	dateTime=models.DateTimeField(null=True, blank=True)
	incident_id=models.IntegerField(null=False, help_text="Incident Id to link to") # Linked to Incident

	def __unicode__(self):              # __unicode__ on Python 2
        	return self.description
