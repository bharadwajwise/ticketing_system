from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from tickets.models import Ticket
from forms import AddTicketForm
from django.core.context_processors import csrf
from django.utils import timezone
from bootstrap_toolkit.widgets import BootstrapUneditableInput
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    ticket_list = Ticket.objects.all()
    t = loader.get_template("tickets/index.html")
    c = Context({
        'ticket_list': ticket_list,
    })
    return HttpResponse(t.render(c))

@login_required(login_url='/login/')
def detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    t = loader.get_template("tickets/ticket.html")
    c = Context({
        'ticket': ticket,
    })
    return HttpResponse(t.render(c))

@login_required(login_url='/login')
def add_ticket(request, user_id):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
	redirect_url = '/user/' + str(user_id) 
	if form.is_valid():
	    new_comment = form.process()
	    ticket_user = User.objects.get(id=user_id)
	    t = Ticket(status = 'in_queue', pub_date = timezone.now(), comment = new_comment, created_by = ticket_user)
	    t.save()
	    return HttpResponseRedirect(redirect_url)
    else:
        form = AddTicketForm()
    	args = {}
    	args.update(csrf(request))
	args['form'] = form
	context = {
	    'user_id': user_id,
	    'form': form,
	}
	return render_to_response('tickets/create_ticket.html', context, RequestContext(request, {
	    'form': form,
	    'layout': layout,
	})) 

def view_ticket(request, user_id):
    userobject = User.objects.get(id=user_id)
    username = userobject.username
    output_ticket = Ticket.objects.filter(created_by=user_id)
    t = loader.get_template('tickets/user_view.html')
    c = Context({
        'user_id': user_id,
     	'output_ticket': output_ticket,
        'username': username,
         })
    return HttpResponse(t.render(c))

def loginview(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('tickets/login.html',c)

def auth_and_login(request, onsuccess='/', onfail='/login/'):
    user = authenticate(username = request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request,user)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

def sign_up(request):
    post = request.POST
    if not user_exists(post['username']):
        user =  create_user(username = post['username'], password=post['password'])
        return auth_and_login(request)
    else:
        return redirect('/login/')

def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    user.save()
    return user

def user_exists(username):
    user_count = User.objects.filter(username = username).count()
    if user_count == 0:
        return False
    return True