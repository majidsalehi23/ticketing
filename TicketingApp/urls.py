from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('load_handlers/', views.load_handlers, name='load_handlers'),
    path('createTicket/', views.createTicket, name='createTicket'),
    path('queryTicket/', views.queryTicket, name='queryTicket'),
    path('showTicket/', views.showTicket, name='showTicket'),
    re_path(r'^listTicket?.*$', views.listTicket, name='listTicket'),
    re_path('reportTicket/', views.reportTicket, name='reportTicket'),
]

publicUrlsString = [
    "/TicketingApp/login/"
]
