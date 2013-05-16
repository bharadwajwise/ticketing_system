from django import forms
from models import Ticket, Ticketuser

class AddTicketForm(forms.ModelForm):
  class Meta:
    model = Ticket
    fields = ('id', 'comment')
  
  def process(self):
    data = self.cleaned_data
    data = data['comment']
    return data
