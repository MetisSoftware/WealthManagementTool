from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from wms.models import Client

# Create your views here.
def index(request):
	return HttpResponse("The time when this page was created is: "+ datetime.datetime.now().strftime("%H:%M"))

def print_client(request):
    client_list = Client.objects.order_by()
    return render_to_response('wms/index.html',{'client_list': client_list})