from django.http import HttpResponse
from tickets.models import Ticketuser, Ticket
from django.template import Context, loader

def index(request):
    ticket_list = Ticket.objects.all()
    t = loader.get_template("tickets/index.html")
    c = Context({
        'ticket_list': ticket_list,
    })
    return HttpResponse(t.render(c))
