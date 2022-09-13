from django.db import models

# Create your models here.
# models.Model is taking in the Model blueprint from the model function within the django.db library 

class Employee(models.Model):

    # the purpose of this string function below is that the names of the objects are returned when executing 
    # Employee.objects.all() in the python shell. 
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    day_rate = models.FloatField()
    cf_number = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    item_image = models.CharField(max_length=500, default="https://eu.evocdn.io/dealer/1065/catalog/product/images/cs_1612369426.png")
   
    
class Risks (models.Model):

    risk_description = models.CharField(max_length = 500)
    risk_impact = models.IntegerField()
    risk_probability = models.IntegerField()
    risk_mitigation = models.CharField(max_length = 500)
    risk_owner = models.CharField(max_length = 200)
    risk_status = models.CharField(max_length = 500)
    date_opened = models.DateField(max_length = 50)


