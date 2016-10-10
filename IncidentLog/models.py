from __future__ import unicode_literals

from django.db import models
from Incident.models import Incident

class IncidentLog(models.Model):
	datetime = models.DateTimeField(help_text="Date and time of log")
	description = models.TextField(help_text="Log description")
	incident_id = models.IntegerField(null=True, help_text="Incident Id this log is related to") # placeholder, f.k later
	#incident_id = models.ForeignKey(Incident, on_delete=models.CASCADE, null=True)
