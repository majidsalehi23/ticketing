import json
import TicketingApp
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from TicketingApp.models import Ticket, Product, Severity, Company, User, State, Role, Action
from TicketingApp.services.AccountingServices import checklogin, editAuthorization, saveTicket
from .common.SessionManager import SessionManager
from .forms import LoginForm, TicketForm, EditTicketForm


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # We check if the data is correct
            user = checklogin(username=username, password=password)
            if user:  # If there is a returned object
                SessionManager.createUserSession(user, user.username, None, None)
                response = redirect('home')
                response.set_cookie('username', username)
                response.set_cookie('session_cookie', SessionManager.getUserCookie(username))
                return response
            else:  # otherwise, an error will be displayed
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def home(request):
    username = request.COOKIES.get('username')
    session = SessionManager.getUserSession(username)
    user = session.user
    ticket_data_list = Ticket.objects.filter(handler=user)
    numberOfTickets = ticket_data_list.count()

    return render(request, 'home.html', {"staffID": user.staffID,
                                         "username": user.username,
                                         "email": user.email,
                                         "company": user.company,
                                         "product": user.product,
                                         "role": user.role,
                                         "numberOfTickets": numberOfTickets,
                                         "ticket_data_list": ticket_data_list,
                                         })


def load_handlers(request):
    # if user and handler are not same, then load the current handler
    username = str(request.COOKIES.get('username'))
    try:
        ticketNumber = request.GET.get('ticketNumber')
        ticket = Ticket.objects.get(ticketNumber=ticketNumber)
        if username != ticket.handler.username:
            authorizedHandlers = TicketingApp.models.User.objects.filter(username=ticket.handler.username)
            return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})
    except:
        pass

    try:
        action = Action.objects.get(id=request.GET.get('action')).name
    except:
        action = "Approved"

    company = request.GET.get('company')
    colleagues = TicketingApp.models.User.objects.filter(company=company)

    if "createTicket" in request.META['HTTP_REFERER']:
        authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Dispatcher"))
        return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})

    role_name = TicketingApp.models.User.objects.get(username=username).role.name

    # if the role is Customer
    if role_name == "Customer":
        if ticket.state.name == "Open":
            authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Dispatcher"))
        elif ticket.state.name == "Customer Review":
            if action == "Approved":
                authorizedHandlers = TicketingApp.models.User.objects.filter(username=ticket.handler.username)
            elif action == "Reject":
                if ticket.severity.name == "Minor":
                    authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Technical Director"))
                elif ticket.severity.name == "Major":
                    authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Manager"))
        return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})

    # if the role is Dispatcher
    elif role_name == "Dispatcher":
        if action == "Approved":
            colleagues = TicketingApp.models.User.objects.filter(company=company)
            authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Engineer"))
        elif action == "Reject":
            authorizedHandlers = TicketingApp.models.User.objects.filter(role=Role.objects.get(name="Customer"))
        return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})

    # if the role is Engineer
    elif role_name == "Engineer":
        colleagues = TicketingApp.models.User.objects.filter(company=company)
        if action == "Approved":
            authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Technical Director"))
        elif action == "Reject":
            authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Dispatcher"))
        return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})

    # if the role is Technical Director
    elif role_name == "Technical Director":
        colleagues = TicketingApp.models.User.objects.filter(company=company)
        if action == "Approved":
            if ticket.severity.name == "Minor":
                authorizedHandlers = TicketingApp.models.User.objects.filter(role=Role.objects.get(name="Customer"))
            elif ticket.severity.name == "Major":
                authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Manager"))
        elif action == "Reject":
            authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Engineer"))
        return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})

    # if the role is Manager
    elif role_name == "Manager":
        if action == "Approved":
            authorizedHandlers = TicketingApp.models.User.objects.filter(role=Role.objects.get(name="Customer"))
        elif action == "Reject":
            colleagues = TicketingApp.models.User.objects.filter(company=company)
            authorizedHandlers = colleagues.filter(role=Role.objects.get(name="Technical Director"))
        return render(request, 'handler_dropdown_list_options.html', {'handlers': authorizedHandlers})


@csrf_exempt
def createTicket(request):
    submitted = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = Ticket()
            ticket.ticketNumber = form.cleaned_data['ticketNumber']
            ticket.company = form.cleaned_data['company']
            ticket.product = form.cleaned_data['product']
            ticket.description = form.cleaned_data['description']
            ticket.handler = form.cleaned_data['handler']
            ticket.state = form.cleaned_data['state']
            ticket.severity = form.cleaned_data['severity']
            saveTicket(request, ticket)
            result = {
                "resultCode": 0
            }
            return HttpResponse(json.dumps(result))
    else:
        form = TicketForm()
        form.fields.get('ticketNumber').disabled = True
        form = TicketForm(initial={'state': State.objects.get(name="Open")})
        form.fields.get('state').disabled = True
        if submitted in request.GET:
            submitted = True

    return render(request, 'createTicket.html', {'form': form, 'submitted': submitted})


def queryTicket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticketNumber = form.cleaned_data["ticketNumber"]
            company = form.cleaned_data["company"]
            product = form.cleaned_data["product"]
            severity = form.cleaned_data["severity"]
            handler = form.cleaned_data["handler"]
            state = form.cleaned_data["state"]
            description = form.cleaned_data["description"]
            # We check if the data is correct

            queryString = ""
            if ticketNumber is not None:
                queryString += "ticketNumber=" + ticketNumber + "&"
            if company is not None:
                queryString += "companyId=" + str(company.id) + "&"
            if product is not None:
                queryString += "productId=" + str(product.id) + "&"
            return redirect("/TicketingApp/listTicket?" + queryString)

    else:
        form = TicketForm()

    return render(request, 'queryTicket.html', {'form': form})


def listTicket(request):
    ticketNumber = request.GET.get("ticketNumber")
    companyId = request.GET.get("companyId")
    productId = request.GET.get("productId")

    query = 'select * from public."TicketingApp_ticket" where '
    if ticketNumber is not None and ticketNumber is not "":
        query += ' "ticketNumber" = ' + ticketNumber + " and "
    if companyId is not None and companyId is not "":
        query += ' company_id = ' + companyId + " and "
    if productId is not None and productId is not "":
        query += ' product_id = ' + productId + " and "

    query = query[:-4]

    ticket_list = Ticket.objects.raw(query)

    if ticket_list:  # If there is a returned object
        response = render(request, 'listTicket.html', {'ticket_data_list': ticket_list})
        return HttpResponse(response)
    else:  # otherwise, an error will be displayed
        return render(request, 'listTicket.html', {'ticket_data_list': []})


@csrf_exempt
def showTicket(request):
    submitted = False
    if request.method == "POST":
        ticketNumber = request.POST.get('ticketNumber')
        ticket = Ticket.objects.get(ticketNumber=ticketNumber)
        ticket.product = Product.objects.get(id=request.POST.get('product'))
        ticket.severity = Severity.objects.get(id=request.POST.get('severity'))
        ticket.company = Company.objects.get(id=request.POST.get('company'))
        ticket.handler = User.objects.get(id=request.POST.get('handler'))
        ticket.state = State.objects.get(id=request.POST.get('state'))
        ticket.description = request.POST.get('description')
        saveTicket(request, ticket)
        result = {
            "resultCode": 0
        }
        return HttpResponse(json.dumps(result))
    else:
        ticketNumber = request.GET.get('id')
        ticket = Ticket.objects.get(ticketNumber=ticketNumber)
        user = User.objects.get(username=request.COOKIES.get('username'))
        ticketHandler = ticket.handler
        initial = {'ticketNumber': ticket.ticketNumber,
                   'product': ticket.product,
                   'severity': ticket.severity,
                   'company': ticket.company,
                   'handler': ticket.handler,
                   'state': ticket.state,
                   'description': ticket.description}
        if user.staffID == ticketHandler.staffID:
            form = EditTicketForm(initial=initial)
        else:
            form = TicketForm(initial=initial)
        form = editAuthorization(form, user, ticketHandler)
        if submitted in request.GET:
            submitted = True
        response = render(request, 'showTicket.html', {'form': form, 'submitted': submitted})

    return response
