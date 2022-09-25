from ast import Delete
from django.db import models
from ii_website import settings
from .choices import status_choices
from .choices import position_choices
from .choices import risk_impact_choices
from .choices import risk_probability_choices
from .choices import risk_owner_choices


# Create your models here.

class Employee(models.Model):

    def __str__(self):
        return self.name

    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, choices=position_choices)
    day_rate = models.FloatField()
    cf_number = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    hours_booked = models.FloatField
    image = models.ImageField(upload_to='images/')
    
class Risk(models.Model):

    risk_description = models.CharField(max_length = 500)
    risk_impact = models.CharField(max_length = 50, choices= risk_impact_choices)
    risk_probability = models.CharField(max_length = 50, choices = risk_probability_choices)
    risk_mitigation = models.CharField(max_length = 500)
    risk_owner = models.CharField(max_length = 200, choices = risk_owner_choices)
    risk_status = models.CharField(max_length = 500, choices= status_choices)
    date_opened = models.DateField()

class Cone (models.Model):

    def __str__(self):
        return self.employee_id

    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    cone_rate = models.FloatField()

class Bookings (models.Model):

    def __str__(self):
        return self.employee_id

    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    week_ending_date = models.DateField()
    hours_booked = models.FloatField()