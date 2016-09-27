from __future__ import unicode_literals

from django.db import models

class IncidentLog(models.Model):
	datetime = models.DateTimeField(help_text="Date and time of log")
	description = models.TextField(help_text="Log description")
