from django.http import HttpResponse
from tickets.models import Ticket

def index(request):
    ticket_list = Ticket.objects.all()
    return HttpResponse(ticket_list) 
