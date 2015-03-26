from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse_lazy

from django.template import RequestContext
from wms.models import Client, ClientForm, Share, Event, Stock, Market, MeetingNotes
from wms import models as m
from wms import scripts
import datetime
import decimal
import json
import math
# Create your views here.


def index(request):
    return render_to_response('wms/index.html', {}, context_instance=RequestContext(request))



def queryAPI(request):
    if(request.method == 'POST'):
        get_args = request.POST
        ni = get_args.get("ni")
        symbol = get_args.get("symbol")
        if symbol == None or symbol == "":
            return HttpResponse(json.dumps({"result":"No Symbol"}), content_type='application/json')
        days = get_args.get("days")
        if days != None:
            days = int(days)
            new_days = days + (math.ceil((days/7))*2)
        else:
            new_days = 9


        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))#Get today and remove 1 day
        yesterday_minus_days = yesterday - datetime.timedelta(days=new_days)
        query = "select * from yahoo.finance.historicaldata where symbol = '"+symbol+\
                "' and startDate = '"+yesterday_minus_days.strftime("%Y-%m-%d")+"' and endDate = '"+\
                yesterday.strftime("%Y-%m-%d")+"'"
        stock_result = scripts.query_api(query)

        if(stock_result["query"]["results"])==None:
            return HttpResponse(json.dumps({"result":"Stock not found"}), content_type='application/json')

        if(new_days >40):
            list = stock_result["query"]["results"]["quote"]
            l =len(list)
            if(new_days <150 ):
                count = math.ceil(l/(3*8))
            elif(new_days < 250):
                count = math.ceil(l/(6*8))
            else:
                count = math.ceil(l/(12*4))
            newStock_result = {"query":{"results":{"quote":[]}}}
            for i in range(1,math.floor(l/count)):
                newStock_result["query"]["results"]["quote"].append(list[i*count])
            stock_result = newStock_result

        if ni==None:
            return HttpResponse(json.dumps(stock_result), content_type='application/json')

        stock = Stock.objects.filter(symbol=symbol)
        if not stock:
            stock_result["shares_owned"] = 0
            stock_result["result"] = "success"
            return HttpResponse(json.dumps(stock_result), content_type='application/json')
        else:
            shares = Share.objects.filter(owner=ni, stock=stock[0])
            total = 0
            for share in shares:
                if share.buy == True:
                    total+= share.amount
                else:
                    total-= share.amount
            stock_result["shares_owned"] = total
            stock_result["result"] = "success"
            return HttpResponse(json.dumps(stock_result), content_type='application/json')

    return HttpResponse(json.dumps({"result":"fail"}), content_type='application/json')


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
        clientTotal = int(client.cash)
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
            Share.objects.create(owner = client, date = date, amount = amount, price = price , stock = stock[0], buy=True )
            stocks = Share.objects.filter(stock=stock[0], owner = client);
            amount = 0
            for s in stocks:
                if s.buy:
                    amount+= s.amount
                else:
                    amount-= s.amount
            return HttpResponse(json.dumps({"result": "success", "stock_amount":amount, "new_amount": str(client.cash)}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"result":"Insufficient funds"}), content_type='application/json')

    return HttpResponse(json.dumps({"result":"fail"}), content_type='application/json')


def sell_stock(request):
    if request.method == "POST":
        get_args = request.POST
        symbol = get_args.get("symbol").upper()
        ni = get_args.get("ni")
        price = float(get_args.get("price"))
        if get_args.get("amount")== None or get_args.get("amount") == "":
            amount = 1
        else:
            amount = int(get_args.get("amount"))
        client = Client.objects.filter(ni_number = ni)[0]
        stock = Stock.objects.filter(symbol= symbol)[0]
        if not stock:
            return HttpResponse(json.dumps({"result":"No such stock"}), content_type='application/json')
        shares = Share.objects.filter(owner=client, stock = stock)
        if not shares:
            return HttpResponse(json.dumps({"result":"No shares"}), content_type='application/json')
        ownedAmount = 0
        for share in shares:
            if share.buy == True:
                ownedAmount += int(share.amount)
            else:
                ownedAmount -= int(share.amount)
        if ownedAmount < amount:
            return HttpResponse(json.dumps({"result": "Not enough stock owned"}), content_type='application/json')
        else:
            total = amount * price
            client.cash += decimal.Decimal(total)
            client.save()
            Share.objects.create(owner=client, date="2015-03-13", price=price, stock=stock, buy=False, amount=amount)
            return HttpResponse(json.dumps({"result": "success", "new_amount": str(client.cash), "stock_amount":ownedAmount}), content_type='application/json')

    return HttpResponse(json.dumps({"result": "fail"}), content_type='application/json')


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
        if amount is None:
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
    clients = Client.objects.filter(fa__ni_number=current_user.ni_number)
    return render_to_response('wms/appointments.html',{'events': events,'clients':clients}, context_instance=RequestContext(request))

@csrf_protect
def create_appointment(request):
    if(request.method == 'POST'):
        post_text = request.POST
        title = post_text.get("title","")
        start = post_text.get("start","")
        end = post_text.get("end","")
        type = post_text.get("type","")
        client = post_text.get("client","")
        if(client!=""):
            c = Client.objects.filter(ni_number=client)[0]
            m.Event.objects.create(fa=request.user, startDateTime=start, endDateTime=end, title=title, type=type, client=c)
        else:
            m.Event.objects.create(fa=request.user, startDateTime=start, endDateTime=end, title=title, type=type)
        event = Event.objects.filter(fa=request.user, startDateTime=start, endDateTime=end, title=title, type=type)[0]
        data = {"result":"success","id":event.id}
        return HttpResponse(
            json.dumps(data),
            content_type='application/json',

        )
    else:
        return render(request,'wms/appointments.html', context_instance=RequestContext(request) )

@login_required
def delete_appointment(request):
    get_params = request.GET
    if(get_params.get('appointment') is None):
        return HttpResponseRedirect('/appointments/')
    else:
        appointment = m.Event.objects.get(id=get_params.get('appointment'))
        appointment.delete()
        return HttpResponseRedirect('/appointments/')

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
            current_user = request.user
            client = form.save(commit=False)
            client.user = request.user
            client.fa = request.user
            print(request.user)
            client.save()
            return HttpResponseRedirect('/clients/')

    return render(request, 'wms/new_client.html', {
        'form': form, 'fa': request.user.pk
    })


@login_required
def delete_client(request):
    get_params = request.GET
    if(get_params.get('client') is None):
        return HttpResponseRedirect('/clients/')
    else:
        client = Client.objects.get(ni_number=get_params.get('client'))
        client.fa = None
        client.save()
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
            sorted_Shares = {}
            owned_shares = {}
            for share in shares:
                if sorted_Shares.get(share.stock.symbol) is None:
                     sorted_Shares[share.stock.symbol]=[share]
                     if share.buy == True:
                        owned_shares[share.stock.symbol] = share.amount
                     else:
                         owned_shares[share.stock.symbol] = -share.amount
                else:
                    sorted_Shares[share.stock.symbol]=sorted_Shares[share.stock.symbol]+[share]
                    if share.buy == True:
                        owned_shares[share.stock.symbol] += share.amount
                    else:
                        owned_shares[share.stock.symbol] -= share.amount


            if client.twitter_username=="":
                twitter = False
            else:
                twitter = True
            return render_to_response('wms/client_details.html',
                                      {'client_details': client,'shares': sorted_Shares,'owned_shares':owned_shares,'twitter':twitter}, context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            return render_to_response('wms/client_details.html',{}, context_instance=RequestContext)


class EditClient(UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'wms/client_update.html'
    success_url = reverse_lazy('print_clients')


class CreateNote(CreateView):
    model = MeetingNotes
    fields = ['event', 'note']
    template_name = 'wms/create_note.html'
    success_url = reverse_lazy('print_clients')

    #def form_valid(self, form):
        #form.instance.client = Client.objects.get(ni_number=self.kwargs['pk'])
        #return super(CreateView, self).form_valid(form)


class ListNotes(ListView):
    model = MeetingNotes

    def get_queryset(self):
        event = Event.objects.filter(client=self.kwargs['pk'])
        return MeetingNotes.objects.filter(event=event)



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
