from tickets.models import Ticket
from django.contrib import admin

class Ticketadmin(admin.ModelAdmin):
        fieldsets = [(None, {'fields': ['status']}), ('Date information',{'fields': ['pub_date']}), (None, {'fields': ['comment']})]

admin.site.register(Ticket, Ticketadmin)
