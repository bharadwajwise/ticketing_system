from django.db import models

# Create your models here.
class Ticket(models.Model):
	status = models.CharField('ticket status', max_length=200)
	pub_date = models.DateTimeField('date created')
	comment = models.CharField('admin comment', max_length=200)

class User(models.Model):
	ticket = models.ForeignKey(Tickets) # change relationship to one-to-many
	username = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=80) #change it to password field
	