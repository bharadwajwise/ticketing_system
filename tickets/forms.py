from django import forms
from models import Ticket
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML, Submit, Div, Row, Button, Field
from crispy_forms.bootstrap import FormActions, PrependedText, AppendedText

class AddTicketForm(forms.ModelForm):
  
  def __init__(self, *args, **kwargs):
    super(AddTicketForm, self).__init__(*args, **kwargs) 
    self.helper = FormHelper(self)
    self.helper.add_input(Submit('submit', 'Add Comment and Ticket'))
     

  class Meta:
    model = Ticket
    fields = ('id', 'comment')
  
  def process(self):
    data = self.cleaned_data
    data = data['comment']
    return data
