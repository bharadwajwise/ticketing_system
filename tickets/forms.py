from django import forms
from models import Ticket, Ticketuser

class AddTicketForm(forms.ModelForm):

  class Meta:
    model = Ticket



