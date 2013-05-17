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
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as authlogin
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.core.exceptions import ObjectDoesNotExist, ErrorHandler

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
def add_ticket(request, requested):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if (int(requested) == int(request.user.pk)):
            if form.is_valid():
                redirect_url = '/user/' + str(request.user.pk)
                new_comment = form.process()
                ticket_user = User.objects.get(id=request.user.pk)
                t = Ticket(status = 'in_queue', pub_date = timezone.now(), comment = new_comment, created_by = ticket_user)
                t.save()
                return HttpResponseRedirect(redirect_url)
        else:
            context = {
                'requested': request.user.pk
            }
            return render_to_response('tickets/restricted_access.html', context)
    else:
        form = AddTicketForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        context = {
        'requested': requested,
        'form': form,
        }
        return render_to_response('tickets/create_ticket.html', context, RequestContext(request, {
	       'form': form,
	       'layout': layout,
        }))

@login_required(login_url='/login')
def view_ticket(request, requested):
    # assert False, "%s" user_id
    if(int(requested) == int(request.session['user_id'])):
        output_ticket = Ticket.objects.filter(created_by = request.user)
        t = loader.get_template('tickets/user_view.html')
        c = Context({
            'output_ticket': output_ticket,
            'username': request.user,
            'user_id': request.user.pk,
            })
        return HttpResponse(t.render(c))
    else:
        context = {
            'user_id': request.session['user_id']
        }
        return render_to_response('tickets/restricted_access.html', context)
    
def loginview(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('tickets/login.html',c)

def auth_and_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                authlogin(request,user)
                user_id = User.objects.get(username= username).id
                request.session['user_id'] = user_id
                output_ticket = Ticket.objects.filter(created_by = request.user)
                context = {
                    'username': username,
                    'user_id': user_id,
                    'output_ticket': output_ticket
                }
                return render_to_response('tickets/user_view.html', context)
            else:
                error = "Account Disabled"
                return errorHandler(error)
        else:
            error = "Invalid username password combination"
            return errorHandler(error)

@login_required
def logout_view(request):
    logout(request)
    try:
        del request.session['user_id']
    except KeyError:
        pass 
    return render_to_response('tickets/logout.html')

def sign_up(request):
    post = request.POST
    if not user_exists(post['username']):
        user =  User.objects.create_user(str(post['username']), str(post['password'])
    return HttpResponseRedirect('/login/')

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