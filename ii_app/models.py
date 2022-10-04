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
    name = models.CharField (max_length=200)
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
        return str((self.hours, self.assignment.resource.name, self.assignment.position))

class Invoice (models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    start = models.DateField()
    end = models.DateField()
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
                return self.project.id


# from ast import Delete
# from django.db import models
# from ii_website import settings
# from .choices import status_choices
# from .choices import position_choices
# from .choices import risk_impact_choices
# from .choices import risk_probability_choices
# from .choices import risk_owner_choices


# # Create your models here.

# class Project(models.Model):

#     def __str__(self):
#         return self.code

#     code = models.CharField(primary_key= True, max_length=200)
#     position = models.CharField(max_length=200, choices=position_choices)
#     day_rate = models.FloatField()
#     cf_number = models.CharField(max_length=200)
#     name = models.CharField(max_length=200)

# class Employee (models.Model):

#     def __str__(self):
#         return self.name

#     id = models.IntegerField(primary_key=True)
#     project = models.ForeignKey(Project,  on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     cone_rate = models.FloatField()
#     image = models.ImageField(upload_to='images/')

# class Risk(models.Model):

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     description = models.CharField(max_length = 500)
#     impact = models.CharField(max_length = 50, choices= risk_impact_choices)
#     probability = models.CharField(max_length = 50, choices = risk_probability_choices)
#     mitigation = models.CharField(max_length = 500)
#     owner = models.CharField(max_length = 200, choices = risk_owner_choices)
#     status = models.CharField(max_length = 500, choices= status_choices)
#     date_opened = models.DateField()


# class Booking (models.Model):

#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     week_ending_date = models.DateField()
#     hours = models.FloatField()

# class Invoice (models.Model):

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     value = models.IntegerField()
#     number = models.IntegerField()
#     date = models.DateField()