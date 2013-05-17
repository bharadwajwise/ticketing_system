from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Ticket(models.Model):
	status = models.CharField('ticket status', max_length=200, blank=True)
	pub_date = models.DateTimeField('date created')
	comment = models.CharField('User comment', max_length=200)
	created_by = models.ForeignKey(User)
	
	def __unicode__(self):
		text = "This ticket was created by: " + str(self.created_by)
		return text