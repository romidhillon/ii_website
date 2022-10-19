from calendar import c
from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.template import loader
from django.db.models import Sum, F, Q
import requests
from django.db.models.functions import Coalesce

from ii_app.forms import RiskForm 
from .models import Project, Resource, Position, Contract, Assignment,  Booking, Invoice, Risk
from .forms import RiskForm
import datetime

# Create your views here.

def main(request):
    resource_names = Resource.objects.all()
    count_of_resources = Resource.objects.count()
    count_of_projects = Project.objects.count()
    assignment_rate = Assignment.objects.all()
    open_risks = Risk.objects.filter(status = 'Open').count()
    date_filter = Booking.objects.filter(day__gte='2022-03-01', day__lte='2019-03-09')
    sum_of_hours = sum(date_filter)
    
    context = {
        'resource_names': resource_names,
        'assignment_rate': assignment_rate,
        'count_of_projects': count_of_projects,
        'count_of_resources': count_of_resources,
        'open_risks': open_risks,
        'sum_of_hours': sum_of_hours,
    }
    return render (request, 'ii_app/dashboard.html',context)


def resources(request):
    query = request.GET.get("query")
    if query:
        resource = Resource.objects.filter(name__icontains = query) 
    else:
        resource = Resource.objects.all()
    context = {
        'resource':resource ,
    }

    return render (request, 'ii_app/resources.html', context)


def resource_detail(request,name):
    
    assignments = Assignment.objects.filter(resource__name = name)

    context = {
        'assignments': assignments ,
    }

    return render (request, 'ii_app/resource_detail.html', context)

def risk_form(request):
    form = RiskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form})


def update_risk_item(request,risk_id):
    risk = Risk.objects.get(id=risk_id)
    form = RiskForm(request.POST or None,instance = risk)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form, 'risk':risk})


def delete_risk_item(request,risk_id):
    risk = Risk.objects.get(id=risk_id)
  
    if request.method =='POST':
        risk.delete()
        return redirect('')
     
    return render (request, 'ii_app/delete_risk_item.html', {'risk':risk})


def risk_register(request):
    risk_register = Risk.objects.all()

    context = {
        'risk_register': risk_register,
    }
    return render (request, 'ii_app/risk_register.html', context)


def margin(request):

    return render (request, 'ii_app/margin.html')


def finances(request):

    query = request.GET.get('query') or ''
    
    projects = Project.objects.filter(title__icontains = query).order_by('code','title')
    
    context = {
        'projects': projects,
    }
    return render (request, 'ii_app/finances.html', context)
    
    

def finance_detail (request, code):
    
    project = Project.objects.get(code=code)
    
    sum_of_invoice_values = project.invoice_set.aggregate(value__sum = Coalesce(Sum('value'),0.00)).get('value__sum')
 
    end = datetime.date.today().replace(day=1)
  
    start = (end - datetime.timedelta(days=1)).replace(day=1)

    period_invoicing = project.position_set.filter(
    assignment__booking__day__gte = start,
	assignment__booking__day__lt = end).aggregate(
	sum = Coalesce(Sum(F('assignment__rate') * F('assignment__booking__hours')), 0.00)).get('sum') 

    life_to_date = project.position_set.filter(
	assignment__booking__day__lt = end).aggregate(
	sum = Coalesce(Sum(F('assignment__rate') * F('assignment__booking__hours')), 0.00)).get('sum') 

    work_in_progress = (life_to_date - sum_of_invoice_values)


    # project margin calculation
    cone_rate_dict = project.resource_set.values('cone_rate') # get the cone rate values 
    cone_rate = cone_rate_dict[0].get('cone_rate')
    hours = Booking.objects.filter(assignment__position__project = project).aggregate(sum=Coalesce(Sum('hours'),0.00)).get('sum')
    total_cost = (cone_rate * hours)
    charge_rate_dict = project.position_set.values('assignment__rate')
    charge_rate = charge_rate_dict[0].get('assignment__rate')
    total_charge = (charge_rate * hours)
    project_margin = round(((total_charge - total_cost)/(total_charge))*100,2) if total_charge else 0
    
    #period margin calculation 
    #period hours 
    #charge rate 

    period_hours = Booking.objects.filter(assignment__position__project = project).filter(
    assignment__booking__day__gte = start,
	assignment__booking__day__lt = end).aggregate(sum = Coalesce(Sum(('assignment__booking__hours')), 0.00)).get('sum')

    cone_rate_dict = project.resource_set.values('cone_rate') 
    cone_rate = cone_rate_dict[0].get('cone_rate')
    charge_rate_dict = project.position_set.values('assignment__rate')
    charge_rate = charge_rate_dict[0].get('assignment__rate')
    period_total_charge = (charge_rate * period_hours)
    period_total_cost = (cone_rate * period_hours)
    period_project_margin = round(((period_total_charge - period_total_cost)/(period_total_charge))*100,2) if period_total_charge else 0
    

    context = {
        'sum_of_invoice_values':sum_of_invoice_values,
        'period_invoicing':period_invoicing,
        'life_to_date':life_to_date,
        'work_in_progress':work_in_progress,
        'project_margin':project_margin,
        'period_project_margin':period_project_margin,
    }

    return render (request, 'ii_app/finance_detail.html', context)

def cv(request):
    resource = Resource.objects.all()

    context = {
        'resource': resource ,
    }

    return render (request, 'ii_app/cv.html', context)


def api(request):
   
    api = requests.get('https://api.covid19api.com/countries').json()
    context = {
        'api':api
    }
    return render (request, 'ii_app/api.html', context)

def search_bar (request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            resources = Resource.objects.filter(name__icontains = query)
            return render (request, 'ii_app/search_bar.html', {'resources': resources})

    else:
        print("your query did not return any results")
        return request (request, 'ii_app/search_bar.html', {})


def search_bar_finances (request):

    query = request.GET.get('query')
    if query:
        projects = Project.objects.filter(title__icontains = query)
    
    else:
        projects = Project.objects.all()

    return render (request, 'ii_app/search_bar_finances.html', {'projects':projects})
