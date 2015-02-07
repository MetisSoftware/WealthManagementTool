from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from wms.models import Client, ClientForm, Share
from wms import models as m
from wms import scripts
import datetime
# Create your views here.


def index(request):
    get_params = request.GET
    symbol = get_params.get("symbol")
    if symbol is None or symbol == "":
        symbol = "GOOG"
    print(get_params.get("symbol"))
    if get_params.get("days") is not None:
        days = int(get_params.get("days"))
    else:
        days = 5
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1))  # Get today and remove 1 day
    yesterdayminus5 = yesterday - datetime.timedelta(days=days)
    query = "select * from yahoo.finance.historicaldata where symbol = '"+symbol+\
            "' and startDate = '"+yesterdayminus5.strftime("%Y-%m-%d")+"' and endDate = '"+\
            yesterday.strftime("%Y-%m-%d")+"'"
    stock_result = scripts.query_api(query)
    return render_to_response('wms/index.html', {'symbol':symbol,'stock_json': stock_result['query']['results']['quote']}, context_instance=RequestContext(request))

    #return render_to_response('wms/index.html',{})


@login_required
def appointments(request):
    return render_to_response('wms/appointments.html', context_instance=RequestContext(request))


@login_required
def print_clients(request):
    current_user = request.user
    client_list = Client.objects.filter(fa__ni_number=current_user.ni_number)
    print(client_list)
    return render_to_response('wms/clients.html', {'client_list': client_list},
                              context_instance=RequestContext(request))


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
def client_details(request):
    get_params = request.GET
    if(get_params.get('client') is None):
        return HttpResponseRedirect('/clients/')
    else:
        try:
            client = Client.objects.get(ni_number=get_params.get('client'))
            shares = Share.objects.filter(owner=get_params.get('client'))
            print(client.twitter_username)
            if client.twitter_username == "":
                twitter = False
            else:
                twitter = True
            return render_to_response('wms/client_details.html',
                                      {'client_details' : client, 'shares' : shares,'twitter' : twitter}, context_instance=RequestContext(request))
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
        return HttpResponseRedirect('wms/appointments.html')
