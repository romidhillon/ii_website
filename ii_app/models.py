from ast import Delete
from django.db import models
from ii_website import settings
from .choices import status_choices
from .choices import position_choices
from .choices import risk_owner_choices
from .choices import risk_probability_choices
# from django.contrib.auth.models import User
from .choices import risk_impact_choices


# Create your models here.


class Client(models.Model):
    name = models.CharField (max_length=200)

    def __str__(self):
         return self.name

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    code = models.CharField (max_length=50)
    title = models.CharField (max_length=200)

    def __str__(self):
         return self.code

class Resource (models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    name = models.CharField (max_length=200)
    amey_position = models.CharField(max_length=100)
    skillset = models.CharField (max_length=500)
    cone_rate = models.FloatField()
    image = models.ImageField()
    cv = models.ImageField()

    def __str__(self):
         return self.name

class Position (models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    name = models.CharField (max_length=200)

    def __str__(self):
         return self.name

class Contract (models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    name = models.CharField (max_length=200)
    start = models.DateField()
    end = models.DateField()
    document = models.ImageField()

    def __str__(self):
        return self.name
    
class Assignment (models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING, related_name= 'resource')
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    rate = models.FloatField()
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
            return self.contract.name

class Booking (models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.DO_NOTHING)
    day = models.DateField()
    hours = models.FloatField()

    def __str__(self):
        return str((self.hours, self.assignment.resource.name, self.assignment.position, 
        self.assignment.resource.project.title, self.day, self.assignment.resource.project.code))

class Invoice (models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    start = models.DateField()
    end = models.DateField()
    value = models.FloatField()
    document = models.ImageField()
    
    def __str__(self):
        return str(self.project.code)

class Risk(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length = 500)
    impact = models.CharField(max_length = 50, choices= risk_impact_choices)
    probability = models.CharField(max_length = 50, choices = risk_probability_choices)
    mitigation = models.CharField(max_length = 500)
    owner = models.CharField(max_length = 200, choices = risk_owner_choices)
    status = models.CharField(max_length = 500, choices= status_choices)
    date_opened = models.DateField()

    def __str__(self):
                return self.id


