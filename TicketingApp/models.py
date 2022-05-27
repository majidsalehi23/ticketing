from django.db import models
from datetime import datetime


class CompanyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(CompanyType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Severity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    staffID = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default="username@company.com")
    company = models.ForeignKey(Company, to_field='id', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.staffID


class State(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    ticketNumber = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    severity = models.ForeignKey(Severity, on_delete=models.CASCADE)
    handler = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.ticketNumber


class TicketLog(models.Model):
    ticketID = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    severity = models.ForeignKey(Severity, on_delete=models.CASCADE, default="")
    handler = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    state = models.ForeignKey(State, on_delete=models.CASCADE, default="")
    description = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.ticketID.ticketNumber


class Action(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
