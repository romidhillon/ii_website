from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader 

# Create your views here.

# whatever name you give to the function, becomes the name of the view 
def main(request):
    return HttpResponse('hello world')


def resources(request):
    return HttpResponse('the information about resources on the account will go on this page')