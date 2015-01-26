from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from wms.models import Client, ClientForm, Share
from wms import models as m
from wms import scripts
import datetime

import json
# Create your views here.


def index(request):
    request.session.set_test_cookie()
    get_params = request.GET
    symbol = get_params.get("symbol")
    if symbol ==None or symbol== "" :
        symbol = "GOOG"
    print(get_params.get("symbol"))
    if get_params.get("days")!=None:
        days = int(get_params.get("days"))
    else:
        days = 5
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))#Get today and remove 1 day
    yesterdayminus5 = yesterday - datetime.timedelta(days=days)
    query = "select * from yahoo.finance.historicaldata where symbol = '"+symbol+\
            "' and startDate = '"+yesterdayminus5.strftime("%Y-%m-%d")+"' and endDate = '"+\
            yesterday.strftime("%Y-%m-%d")+"'"
    stock_result = scripts.query_api(query)
    return render_to_response('wms/index.html', {'symbol':symbol,'stock_json': stock_result['query']['results']['quote']})

    #return render_to_response('wms/index.html',{})


def appointments(request):
    if request.session.test_cookie_worked():
        print ("TEST cookie worked!")
        request.session.delete_test_cookie()
    return render_to_response('wms/appointments.html')


def print_clients(request):
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
            twitter_username = form.cleaned_data['twitter_username']
            twitter_widget_id = form.cleaned_data['twitter_widget_id']
            post = m.Client.objects.create(
                first_name = first_name, surname = surname, email = email, \
                mob_phone = mob_phone, home_phone = home_phone, dob = dob, \
                ni_number = ni_number, fa = fa, cash = cash, \
                twitter_username = twitter_username, twitter_widget_id = twitter_widget_id)
            return HttpResponseRedirect('/clients/')

    return render(request, 'wms/new_client.html', {
        'form': form,
    })

def client_details(request):
    get_params = request.GET
    if(get_params.get('client')==None):
        return HttpResponseRedirect('/clients/')
    else:
        try:
            client = Client.objects.get(ni_number=get_params.get('client'))
            shares = Share.objects.filter(owner=get_params.get('client'))
            print(client.twitter_username)
            if client.twitter_username=="":
                twitter = False
            else:
                twitter = True
            return render_to_response('wms/client_details.html',
                                      {'client_details': client,'shares': shares,'twitter':twitter})
        except ObjectDoesNotExist:
            return render_to_response('wms/client_details.html',{})


class LoginView(FormView):
    template_name = 'wms/login.html'
    form_class = AuthenticationForm
    success_url = 'wms/index.html'

    def form_valid(self, form):
        user = authenticate(username=self.request.POST['username'],
                            password=self.request.POST['password'])
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect('wms/index.html')
        return HttpResponseRedirect('wms/index.html')
