from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('load_handlers/', views.load_handlers, name='load_handlers'),
    path('createTicket/', views.createTicket, name='createTicket'),
    path('queryTicket/', views.queryTicket, name='queryTicket'),
    path('showTicket/', views.showTicket, name='showTicket'),
]

publicUrlsString = [
    "/TicketingApp/login/"
]
