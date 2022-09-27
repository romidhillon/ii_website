from ast import Delete
from django.db import models
from ii_website import settings
from .choices import status_choices
from .choices import position_choices
from .choices import risk_impact_choices
from .choices import risk_probability_choices
from .choices import risk_owner_choices


# Create your models here.

class Project(models.Model):

    def __str__(self):
        return self.code

    code = models.CharField(primary_key= True, max_length=200)
    position = models.CharField(max_length=200, choices=position_choices)
    day_rate = models.FloatField()
    cf_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class Employee (models.Model):

    def __str__(self):
        return self.name

    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(Project,  on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')

class Risk(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length = 500)
    impact = models.CharField(max_length = 50, choices= risk_impact_choices)
    probability = models.CharField(max_length = 50, choices = risk_probability_choices)
    mitigation = models.CharField(max_length = 500)
    owner = models.CharField(max_length = 200, choices = risk_owner_choices)
    status = models.CharField(max_length = 500, choices= status_choices)
    date_opened = models.DateField()

class Cone (models.Model):

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rate = models.FloatField()

class Booking (models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    week_ending_date = models.DateField()
    hours = models.FloatField()

class Invoice (models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    value = models.IntegerField()
    number = models.IntegerField()
    date = models.DateField()