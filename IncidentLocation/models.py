from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

def validate_positive_num(value):
	if value < 0:
		raise ValidationError("Field content of %f is not a positive number" % value)

class IncidentLocation(models.Model):
	radius = models.FloatField(
		help_text="Radius of the incident",
		validators=[validate_positive_num]
		)
	coord_lat = models.FloatField(help_text="Latitude coordinate of the incident")
	coord_long = models.FloatField(help_text="Longitude coordinate of the incident")


