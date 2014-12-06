from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from wms.models import Client, ClientForm
from wms import models as m
from wms import scripts
import datetime
import json
# Create your views here.


def index(request):
    get_params = request.GET
    print(get_params.get("symbol"))
    if get_params.get("symbol")!=None:
        if get_params.get("days")!=None:
            days = int(get_params.get("days"))
        else:
            days = 5
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))#Get today and remove 1 day
        yesterdayminus5 = yesterday - datetime.timedelta(days=days)
        query = "select * from yahoo.finance.historicaldata where symbol = '"+get_params.get("symbol")+\
                                     "' and startDate = '"+yesterdayminus5.strftime("%Y-%m-%d")+"' and endDate = '"+\
                                     yesterday.strftime("%Y-%m-%d")+"'"
        stock_result = scripts.query_api(query)
        print(stock_result['query']['results']['quote'])
        return render_to_response('wms/index.html', {'symbol':get_params.get("symbol"),'stock_json': stock_result['query']['results']['quote']})

    return HttpResponseRedirect('index.html')
    
def appointments(request):
    return render_to_response('wms/appointments.html')


def print_client(request):
    get_params = request.GET
    if get_params.get("fa")!=None:
        client_list = Client.objects.filter(fa__ni_number=get_params.get("fa"))
        print(client_list)
        return render_to_response('wms/clients.html', {'client_list': client_list})

    client_list = Client.objects.order_by()
    return render_to_response('wms/clients.html', {'client_list': client_list})


def new_client(request):
    if request.method == 'GET':
        form = ClientForm()
    else:
        # Bind data from reqtest.Post into a ClientForm
        form = ClientForm(request.POST)
        # Check if data is valid then redirect user (temporary measure)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            mob_phone = form.cleaned_data['mob_phone']
            home_phone = form.cleaned_data['home_phone']
            dob = form.cleaned_data['dob']
            ni_number = form.cleaned_data['ni_number']
            fa = form.cleaned_data['fa']
            cash = form.cleaned_data['cash']
            post = m.Client.objects.create(
                first_name = first_name, surname = surname, email = email, \
                mob_phone = mob_phone, home_phone = home_phone, dob = dob, \
                ni_number = ni_number, fa = fa, cash = cash)
            return HttpResponseRedirect('/clients/')

    return render(request, 'wms/new_client.html', {
        'form': form,
        })
