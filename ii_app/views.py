from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.template import loader

from ii_app.forms import RiskForm 
from .models import Employee
from .forms import RiskForm

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


def risk_form(request):
    form = RiskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('ii_app/home.html')

    return render (request, 'ii_app/risk_form.html', {'form':form})


def margin(request):
    return render (request, 'ii_app/margin.html')