from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('load_handlers/', views.load_handlers, name='load_handlers'),
    path('createTicket/', views.createTicket, name='createTicket'),
    path('queryTicket/', views.queryTicket, name='queryTicket'),
    path('showTicket/', views.showTicket, name='showTicket'),
    # re_path(r'^listTicket/(?:ticketNumber-(?P<ticketNumber>\d+)/)?$', views.listTicket, name='listTicket'),
    re_path(r'^listTicket?.*$', views.listTicket, name='listTicket'),
]

publicUrlsString = [
    "/TicketingApp/login/"
]
