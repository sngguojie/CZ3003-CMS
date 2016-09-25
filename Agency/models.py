from __future__ import unicode_literals

from django.db import models

# Create your models here.
agency_id=models.AutoField(primary_key=True)
name=models.TextField()
description=models.TextField()
sms_contact_no=models.CharField(max_length=8)
def __unicode__(self):
	return self.description
