from calendar import c
from django.shortcuts import render, redirect 
from django.shortcuts import HttpResponse
from django.template import loader
from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce
from datetime import date, timedelta
from django.contrib import messages
from django.core.paginator import Paginator
import requests

from ii_app.forms import RiskForm, BookingForm
from django.forms import modelformset_factory 
from .models import Project, Resource, Position, Contract, Assignment,  Booking, Invoice, Risk
from .forms import RiskForm, BookingForm, FileUploadForm
import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view 
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

@login_required(login_url = 'sign_in')
def main(request):
    resource_names = Resource.objects.all()
    count_of_resources = Resource.objects.count()
    count_of_projects = Project.objects.count()
    assignment_rate = Assignment.objects.all()
    open_risks = Risk.objects.filter(status = 'Open').count()
    date_filter = Booking.objects.filter(day__gte='2022-03-01', day__lte='2019-03-09')
    sum_of_hours = sum(date_filter)
    count_of_bookings = Risk.objects.filter(status = 'open')
  

    
    context = {
        'resource_names': resource_names,
        'assignment_rate': assignment_rate,
        'count_of_projects': count_of_projects,
        'count_of_resources': count_of_resources,
        'open_risks': open_risks,
        'sum_of_hours': sum_of_hours,
        'count_of_bookings': count_of_bookings
    }
    return render (request, 'ii_app/dashboard.html',context)

@login_required(login_url = 'sign_in')
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

@login_required(login_url = 'sign_in')
def resource_detail(request,name):
    
    assignments = Assignment.objects.filter(resource__name = name)

    context = {
        'assignments': assignments ,
    }

    return render (request, 'ii_app/resource_detail.html', context)

@login_required(login_url = 'sign_in')
def risk_form(request):
    form = RiskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form})

@login_required(login_url = 'sign_in')
def update_risk_item(request,risk_id):
    item = Risk.objects.get(id=risk_id)
    form = RiskForm(request.POST or None,instance = item)

    if form.is_valid():
        form.save()
        return redirect('')

    return render (request, 'ii_app/risk_form.html', {'form':form, 'item':item})

@login_required(login_url = 'sign_in')
def delete_risk_item(request,risk_id):
    item = Risk.objects.get(id=risk_id)
  
    if request.method =='POST':
        item.delete()
        return redirect('')
     
    return render (request, 'ii_app/delete_risk_item.html', {'item':item})

@login_required(login_url = 'sign_in')
def risk_register(request):

    query = request.GET.get('query') or ''

    risk_register = Risk.objects.filter(Q(owner__icontains = query) | Q(status__icontains = query))

    context = {
        'risk_register': risk_register,
    }
    return render (request, 'ii_app/risk_register.html', context)

@login_required(login_url = 'sign_in')
def margin(request):

    return render (request, 'ii_app/margin.html')

@login_required(login_url = 'sign_in')
def finances(request):

    query = request.GET.get('query') or ''
    
    projects = Project.objects.filter(title__icontains = query).order_by('code','title')
    
    context = {
        'projects': projects,
    }
    return render (request, 'ii_app/finances.html', context)
    
    
@login_required(login_url = 'sign_in')
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

@login_required(login_url = 'sign_in')
def cv(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        file = request.FILES['file']
        
    else:
        form = FileUploadForm()

    resource = Resource.objects.all()

    context = {
        'resource': resource ,
        'form':form
    }

    return render (request, 'ii_app/cv.html', context)

@login_required(login_url = 'sign_in')
def api(request):
   
    api = requests.get('https://api.covid19api.com/countries').json()
    context = {
        'api':api
    }
    return render (request, 'ii_app/api.html', context)

@login_required(login_url = 'sign_in')
def search_bar (request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            resources = Resource.objects.filter(name__icontains = query)
            return render (request, 'ii_app/search_bar.html', {'resources': resources})

    else:
        print("your query did not return any results")
        return request (request, 'ii_app/search_bar.html', {})

@login_required(login_url = 'sign_in')
def bookings (request):

   query = request.GET.get('query') or ''
    
   resource_info = Assignment.objects.filter(Q(resource__name__icontains = query) |Q(position__project__code = query))
    
   context = {
        'resource_info': resource_info,
    }
   return render (request, 'ii_app/bookings.html', context)

@login_required(login_url = 'sign_in')
def booking_form(request,assignment_code):

    assignment = Assignment.objects.get(pk=assignment_code)
    week_start = date.today()
    week_start -= timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=4)
    day_dict = {
        'monday':week_start,
        'tuesday': week_start + timedelta(days = 1),
        'wednesday':  week_start + timedelta(days = 2),
        'thursday':  week_start + timedelta(days = 3),
        'friday':  week_start + timedelta(days = 4),
    }

    day_dict_2 = [value.strftime('%d-%m-%Y') for key,value in day_dict.items()]

    bookings = assignment.booking_set.filter(day__gte=week_start, day__lte=week_end)
    booking_dict = {booking.day.strftime('%A').lower():booking for booking in bookings}
   
    form = BookingForm(initial={key:value.hours for key,value in booking_dict.items()})
    print(request.POST)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            for key,value in form.cleaned_data.items():
                if key in booking_dict:
                    booking_dict[key].hours = value
                    booking_dict[key].save()
                else:
                    booking = assignment.booking_set.create(day = day_dict[key], hours = value)
        #     messages.success(request,"Timesheet submitted successfully")
            return redirect(f'/ii_app/bookings/{assignment_code}')
      

    context = {
        'form':form,
        'week_end':week_end,
        'day_dict':day_dict_2,
        'zipped':zip(form,day_dict_2)
    }

    return render (request, 'ii_app/booking_form.html', context)

@api_view(['GET','POST'])

def project_list_api (request):

    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many = True)
        return JsonResponse({'projects':serializer.data})
    
    if request.method == 'POST':
        serializer = ProjectSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'DELETE'])
def project_list_api_detail (request,id):

    try: 
        project = Project.objects.get(pk = id)
    except Project.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

# get all the projects 
# serialize them 
# return json