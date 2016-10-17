from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CMSStatus(models.Model):
	
	active = models.BooleanField(default=False)



