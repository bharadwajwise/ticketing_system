from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from tickets.models import Ticket, Ticketuser
from forms import AddTicketForm
from django.core.context_processors import csrf
from django.utils import timezone

from bootstrap_toolkit.widgets import BootstrapUneditableInput

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
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
	redirect_url = '/user/' + str(userid) 
	if form.is_valid():
	    new_comment = form.process()
	    ticket_user = Ticketuser.objects.get(id=userid)
	    t = Ticket(status = 'in_queue', pub_date = timezone.now(), comment = new_comment, created_by = ticket_user)
	    t.save()
	    return HttpResponseRedirect(redirect_url)
    else:
        form = AddTicketForm()
    	args = {}
    	args.update(csrf(request))
	args['form'] = form
	t = loader.get_template('tickets/create_ticket.html')
	context = {
	    'user_id': userid,
	    'form': form,
	}
	return render_to_response('tickets/create_ticket.html', context, RequestContext(request, {
	    'form': form,
	    'layout': layout,
	})) 

def view_ticket(request, userid):
    user_id = userid
    output_ticket = Ticket.objects.filter(created_by=userid)
    t = loader.get_template('tickets/user_view.html')
    c = Context({
         'user_id': userid,
	 'output_ticket': output_ticket,
         })
    return HttpResponse(t.render(c))
