import time
from django import forms
import TicketingApp
from TicketingApp.models import Ticket, Company, Product, Severity, State, Action


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class TicketForm(forms.Form):
    ticketNumber = forms.CharField(max_length=50, required=False, initial="user" + "-" + str(time.time())[0:10],
                                   widget=forms.TextInput(attrs={'class': "form-control"}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False,
                                     widget=forms.Select(attrs={'class': "form-select"}))
    severity = forms.ModelChoiceField(queryset=Severity.objects.all(), required=False,
                                      widget=forms.Select(attrs={'class': "form-select"}))
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False,
                                     widget=forms.Select(attrs={'class': "form-select"}))
    handler = forms.ModelChoiceField(queryset=TicketingApp.models.User.objects.all(), required=False,
                                     widget=forms.Select(attrs={'class': "form-select"}))
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False,
                                   widget=forms.Select(attrs={'class': "form-select"}))
    description = forms.CharField(max_length=500, required=False,
                                  widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['handler'].queryset = TicketingApp.models.User.objects.none()
        self.fields['ticketNumber'].initial = "user" + "-" + str(time.time())[0:10]

        if 'company' in self.data:
            try:
                company = int(self.data.get('company'))
                self.fields['handler'].queryset = TicketingApp.models.User.objects.filter(company=company)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty User queryset
        else:
            self.fields['handler'].queryset = TicketingApp.models.User.objects.all()


class EditTicketForm(TicketForm):
    action = forms.ModelChoiceField(queryset=Action.objects.all(), required=True, initial=Action.objects.get(id=1))
