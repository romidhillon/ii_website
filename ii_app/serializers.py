from rest_framework import serializers
from .models import Project

# this file describes the process from going from a python object to a JSON file. 

class ProjectSerializer (serializers.ModelSerializer):
    class Meta: 
        model = Project
        fields = ['id', 'client', 'code','title']




