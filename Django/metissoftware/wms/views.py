from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.template import RequestContext
from wms.models import Client, ClientForm, Share, Event, Stock, Market
from wms import models as m
from wms import scripts
import datetime
import decimal
import json
# Create your views here.


def index(request):
    get_params = request.GET
    symbol = get_params.get("symbol")
    if symbol is None or symbol=="":
        symbol = "GOOG"
    if get_params.get("days") is not None:
        days = int(get_params.get("days"))
    else:
        days = 5
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))#Get today and remove 1 day
        yesterdayminus5 = yesterday - datetime.timedelta(days=days)
        query = "select * from yahoo.finance.historicaldata where symbol = '"+symbol+\
            "' and startDate = '"+yesterdayminus5.strftime("%Y-%m-%d")+"' and endDate = '"+\
            yesterday.strftime("%Y-%m-%d")+"'"
        stock_result = scripts.query_api(query)
        return render_to_response('wms/index.html', {'symbol':symbol,'stock_json': stock_result['query']['results']['quote']}, context_instance=RequestContext(request))

    #return render_to_response('wms/index.html',{})

def queryAPI(request):
    if(request.method == 'POST'):
        get_args = request.POST
        symbol = get_args.get("symbol")
        if symbol == None or symbol == "":
            return;
        days = get_args.get("days")
        if days != None:
            days = int(days);
        else:
            days = 5
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))#Get today and remove 1 day
        yesterday_minus_days = yesterday - datetime.timedelta(days=days)
        query = "select * from yahoo.finance.historicaldata where symbol = '"+symbol+\
                "' and startDate = '"+yesterday_minus_days.strftime("%Y-%m-%d")+"' and endDate = '"+\
                yesterday.strftime("%Y-%m-%d")+"'"
        stock_result = scripts.query_api(query)

    return HttpResponse(json.dumps(stock_result), content_type='application/json')

def buyStock(request):
    if(request.method == 'POST'):
        get_args = request.POST
        symbol = get_args.get("symbol").upper()
        ni = get_args.get("ni")
        price = float(get_args.get("price"))
        amount = get_args.get("amount")
        if get_args.get("amount")== None or get_args.get("amount") == "":
            amount = 1
        else:
            amount = int(get_args.get("amount"))
        date = get_args.get("date")
        if symbol == None or symbol == "":
            return;
        client = Client.objects.filter(ni_number = ni)[0]
        requestTotal = amount*price
        clientTotal = client.cash
        if(clientTotal>=requestTotal):
            client.cash-=decimal.Decimal(requestTotal)
            client.save()
            stock = Stock.objects.filter(symbol=symbol)
            if not stock:
                query = "select * from yahoo.finance.quote where symbol = '"+symbol+"'"
                stock_result = scripts.query_api(query)
                stock_result = stock_result['query']['results']['quote']
                market = Market.objects.filter(name = stock_result['StockExchange'])
                if not market:
                    Market.objects.create(name = stock_result['StockExchange'], full_name="")
                    market = Market.objects.filter(name = stock_result['StockExchange'])
                Stock.objects.create(symbol=stock_result['Symbol'], company=stock_result['Name'], market=market[0])
            stock = Stock.objects.filter(symbol=symbol)
            Share.objects.create(owner = client, buy_date = date, amount = amount, price = price , stock = stock[0] )
            return HttpResponse(json.dumps({"result": "success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"result":"Insufficient funds"}), content_type='application/json')

    return HttpResponse(json.dumps({"result":"fail"}), content_type='application/json')

def deposit_cash(request):
    if(request.method == 'POST'):
        get_args = request.POST
        ni = get_args.get("ni")
        amount = get_args.get("amount")
        client = Client.objects.filter(ni_number=ni)
        if amount == "":
            return HttpResponse(json.dumps({"result":"amount_error"}), content_type='application/json')
        if not client:
            return HttpResponse(json.dumps({"result":"Client not found"}), content_type='application/json')
        client = client[0]
        cash = client.cash + decimal.Decimal(amount)
        client.cash = cash
        client.save()
        return HttpResponse(json.dumps({"result": "success","new_amount":str(cash)}), content_type='application/json')

def withdraw_cash(request):
    if(request.method == 'POST'):
        get_args = request.POST
        ni = get_args.get("ni")
        amount = get_args.get("amount")
        client = Client.objects.filter(ni_number=ni)
        if amount == "":
            return HttpResponse(json.dumps({"result":"amount_error"}), content_type='application/json')
        if not client:
            return HttpResponse(json.dumps({"result":"Client not found"}), content_type='application/json')
        client = client[0]
        amount = decimal.Decimal(amount)
        if client.cash < amount:
            return HttpResponse(json.dumps({"result":"Insufficient funds"}), content_type='application/json')
        cash = client.cash - amount
        client.cash = cash
        client.save()
        return HttpResponse(json.dumps({"result": "success","new_amount":str(cash)}), content_type='application/json')

@login_required
def appointments(request):
    current_user = request.user
    events = Event.objects.filter(fa__ni_number=current_user.ni_number)
    return render_to_response('wms/appointments.html',{'events': events}, context_instance=RequestContext(request))

@csrf_protect
def create_appointment(request):
    if(request.method == 'POST'):
        post_text = request.POST
        title = post_text.get("title","")
        start = post_text.get("start","")
        end = post_text.get("end","")
        type = post_text.get("type","")
        m.Event.objects.create(fa=request.user, startDateTime=start, endDateTime=end, title=title, type=type)
        print("pass")
        data = {"success":"success"};
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',

        )
    else:
        return render(request,'wms/appointments.html', context_instance=RequestContext(request) )

@login_required
def print_clients(request):
    current_user = request.user
    client_list = Client.objects.filter(fa__ni_number=current_user.ni_number)
    print(client_list)
    return render_to_response('wms/clients.html', {'client_list': client_list}, context_instance=RequestContext(request))



@login_required
def new_client(request):
    if request.method == 'GET':
        form = ClientForm()
    else:
        # Bind data from reqtest.Post into a ClientForm
        form = ClientForm(request.POST, request.FILES)
        # Check if data is valid then redirect user (temporary measure)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return HttpResponseRedirect('/clients/')

    return render(request, 'wms/new_client.html', {
        'form': form,
    })

@login_required
def delete_client(request):
    get_params = request.GET
    if(get_params.get('client') is None):
        return HttpResponseRedirect('/clients/')
    else:
        client = Client.objects.get(ni_number=get_params.get('client'))
        client.delete()
        return HttpResponseRedirect('/clients/')


@login_required
def client_details(request):
    get_params = request.GET
    if(get_params.get('client') is None):
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
                                         {'client_details': client,'shares': shares,'twitter':twitter}, context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            return render_to_response('wms/client_details.html',{}, context_instance=RequestContext)


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
