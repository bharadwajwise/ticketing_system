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

def view_ticket(request, userid):
    output_ticket = Ticket.objects.get(created_by=userid)
    output_id = output_ticket.id
    output_status = output_ticket.status
    output_comment = output_ticket.comment
    output_format = "Ticket no. " + str(output_id) + " has been created by you. Status: " + output_status + " Comments: " + output_comment
    return HttpResponse(output_format)
