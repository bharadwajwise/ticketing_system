from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from tickets.models import Ticket, Ticketuser
from forms import AddTicketForm
from django.core.context_processors import csrf

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

def add_ticket(request, userid):
   if request.POST:
	form = AddTicketForm(request.POST)
	if form.is_valid():
	    form.save()
	
	    return HttpResponseRedirect('/user/userid')
    else:
	form = AddTicketForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('add_ticket.html', args) 

def view_ticket(request, userid):
    user_id = userid
    output_ticket = Ticket.objects.get(created_by=userid)
    output_id = output_ticket.id
    output_status = output_ticket.status
    output_comment = output_ticket.comment
    t = loader.get_template('tickets/user_view.html')
    c = Context({
         'user_id': userid,
	 'output_ticket': output_ticket,
         'output_id': output_id,
         'output_status': output_status,
         'output_comment': output_comment,
    })
    return HttpResponse(t.render(c))
