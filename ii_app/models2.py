from ast import Delete
from django.db import models
from ii_website import settings
from .choices import status_choices
from .choices import position_choices
from .choices import risk_impact_choices
from .choices import risk_probability_choices
from .choices import risk_owner_choices
# from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField (max_length=200)

class Project(models.Model):
    client = models.ForeignKey(Client)
    code = models.CharField (max_length=50)
    title = models.CharField (max_length=200)

class Resource (models.Model):
    name = models.CharField (max_length=200)
    skillset = models.CharField (max_length=200)
    cone_rate = models.FloatField()

class Position (models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField (max_length=200)

class Contract (models.Model):
    project = models.ForeignKey(Project)
    start = models.DateField()
    end = models.DateField()
    file = models.ImageField()
    
class Assignment (models.Model):
    resource = models.ForeignKey(Resource)
    position = models.ForeignKey(Position)
    contract = models.ForeignKey(Contract)
    rate = models.FloatField()
    start = models.DateField()
    end = models.DateField()

class Booking (models.Model):
    assignment = models.ForeignKey(Assignment)
    day = models.DateField()
    hours = models.FloatField()

class Invoice (models.Model):
    project = models.ForeignKey(Project)
    start = models.DateField()
    end = models.DateField()
    file = models.ImageField()

class Risk(models.Model):
    project = models.ForeignKey(Project)
    resource = models.ForeignKey(Resource)
    description = models.CharField(max_length = 500)
    impact = models.CharField(max_length = 50, choices= risk_impact_choices)
    probability = models.CharField(max_length = 50, choices = risk_probability_choices)
    mitigation = models.CharField(max_length = 500)
    owner = models.CharField(max_length = 200, choices = risk_owner_choices)
    status = models.CharField(max_length = 500, choices= status_choices)
    date_opened = models.DateField()