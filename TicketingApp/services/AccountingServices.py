import TicketingApp
from TicketingApp.models import User, State


def checklogin(username, password):
    return User.objects.get(username=username, password=password)


def editAuthorization(form, user, ticketHandler):
    form.fields.get('ticketNumber').disabled = True
    form.fields.get('state').disabled = True
    if user.staffID != ticketHandler.staffID or form.initial.get('state').name == "Close":
        for field_name in form.fields:
            form.fields[field_name].disabled = True

    elif user.role.name in ["Dispatcher", "Engineer", "Technical Director", "Manager"]:
        form.fields.get('product').disabled = True
        form.fields.get('severity').disabled = True
        form.fields.get('company').disabled = True

    elif user.role.name == "Customer" and form.initial.get('state').name == "Customer Review":
        form.fields.get('product').disabled = True
        form.fields.get('severity').disabled = True
        form.fields.get('company').disabled = True

    return form


def saveTicket(request, ticket):
    # Ajax sends 1, the private key of "Approved", as string.
    if request.path == "/TicketingApp/createTicket/" or request.POST.get('action') == "1":
        if ticket.state.name == "Final Technical Review":
            if ticket.severity.name == "Minor":
                ticket.state = State.objects.get(id=ticket.state.id + 2)
        ticket.state = State.objects.get(id=ticket.state.id + 1)
    # Ajax sends 2, the private key of "Reject", as string.
    elif request.POST.get('action') == "2":
        if ticket.state.name == "Customer Review":
            if ticket.severity.name == "Minor":
                ticket.state = State.objects.get(id=ticket.state.id - 2)
        ticket.state = State.objects.get(id=ticket.state.id - 1)
    ticket.save()
