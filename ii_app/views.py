from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader 
from .models import Employee

# Create your views here.

# whatever name you give to the function, becomes the name of the view 
def main(request):
    return render (request, 'ii_app/home.html')


def resources(request):
    employees = Employee.objects.all()
    context = {
        'employee_list': employees,
    }
    return render (request, 'ii_app/resources.html', context)


def resource_detail(request,employee_id):
    employee = Employee.objects.get(id = employee_id)
    context = {
        'employee': employee,
    }
    return render (request, 'ii_app/resource_detail.html', context)


def risks(request):
    return render (request, 'ii_app/risks.html')
