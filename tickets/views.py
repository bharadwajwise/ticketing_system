from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from tickets.models import Ticket, Ticketuser
from forms import AddTicketForm
from django.core.context_processors import csrf
from django.utils import timezone

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
	redirect_url_2 = 'tickets/create_ticket.html'
	return render_to_response(redirect_url_2, context, context_instance=RequestContext(request))
# return HttpResponse(t.render(c)) 

def view_ticket(request, userid):
    user_id = userid
    output_ticket = Ticket.objects.filter(created_by=userid)
    # assert False,"output_tickets--- %s"%output_ticket
    # output_id = output_ticket.id
    # output_status = output_ticket.status
    # output_comment = output_ticket.comment
    t = loader.get_template('tickets/user_view.html')
    c = Context({
         'user_id': userid,
	 'output_ticket': output_ticket,
         })
    return HttpResponse(t.render(c))
