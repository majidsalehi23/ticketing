function toJson(data) {
    data = JSON.parse(data);
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            try {
                data[key] = toJson(data[key]);
            } catch (e) {
                console.log("cannot parse: " + data[key], " it is probably a leaf.");
            }
        }
    }
    return data;
}

function createTicket() {
    debugger;
    console.log('saving ticket');
    let ticketNumber = $('#id_ticketNumber')
    let product = $('#id_product')
    let severity = $('#id_severity')
    let company = $('#id_company')
    let handler = $('#id_handler')
    let state = $('#id_state')
    let description = $('#id_description')

    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:8000/TicketingApp/createTicket/?submitted=True",
        data: {
            ticketNumber: ticketNumber.val(),
            company: company.val(),
            product: product.val(),
            handler: handler.val(),
            severity: severity.val(),
            state: state.val(),
            description: description.val()
        }
    }).done(function(result) {
        debugger;
        data = toJson(result)
        if (data.resultCode == 0) {
            company.val(''),
                product.val(''),
                handler.val(''),
                severity.val(''),
                state.val(''),
                description.val('')
            alert("ticket created");
            window.location.href = "/TicketingApp/home";
        }
    });
}

function updateTicket() {
    debugger;
    console.log('saving ticket');
    let ticketNumber = $('#id_ticketNumber')
    let product = $('#id_product')
    let severity = $('#id_severity')
    let company = $('#id_company')
    let handler = $('#id_handler')
    let state = $('#id_state')
    let description = $('#id_description')
    let action = $('#id_action')

    $.ajax({
        method: "POST",
        url: "http://127.0.0.1:8000/TicketingApp/showTicket/?submitted=True",
        data: {
            ticketNumber: ticketNumber.val(),
            company: company.val(),
            product: product.val(),
            handler: handler.val(),
            severity: severity.val(),
            state: state.val(),
            description: description.val(),
            action: action.val()
        }
    }).done(function(result) {
        debugger;
        data = toJson(result)
        if (data.resultCode == 0) {
            company.val(''),
                product.val(''),
                handler.val(''),
                severity.val(''),
                state.val(''),
                description.val(''),
                action.val('')
            alert("ticket updated");
            window.location.href = "/TicketingApp/home";
        }
    });
}

function showTicket(t) {
    window.location.href = "/TicketingApp/showTicket?id=" + t;
}


function reportTicket(t) {
    console.log(t)
    window.location.href = "/TicketingApp/reportTicket?id=" + t;
}
