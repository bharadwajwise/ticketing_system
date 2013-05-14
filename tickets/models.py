from django.db import models
import datetime
from django.utils import timezone

class User(models.Model):
        username = models.CharField(max_length=200)

        def __unicode__(self):
                return self.username

class Ticket(models.Model):
	status = models.CharField('ticket status', max_length=200)
	pub_date = models.DateTimeField('date created')
	comment = models.CharField('manager comment', max_length=200)
        created_by = models.ForeignKey(User) 
        
	def __unicode__(self):
		return self.status
