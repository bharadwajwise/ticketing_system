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

def detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    t = loader.get_template("tickets/ticket.html")
    c = Context({
        'ticket': ticket,
    })
    return HttpResponse(t.render(c))

def add_ticket(request):
    return HttpResponse("Here you can add new tickets")
