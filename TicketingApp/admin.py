from django.contrib import admin
from .models import *

admin.site.register(CompanyType)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Role)
admin.site.register(Severity)
admin.site.register(User)
admin.site.register(State)
admin.site.register(Ticket)
admin.site.register(TicketLog)
admin.site.register(Action)
