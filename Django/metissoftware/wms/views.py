from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime
from wms.models import Client
from wms.forms import ClientForm
from wms import models as m
from django.core.urlresolvers import reverse

# Create your views here.


def index(request):
    return HttpResponse("The time when this page was created is: "
                        + datetime.datetime.now().strftime("%H:%M"))


def print_client(request):
    client_list = Client.objects.order_by()
    return render_to_response('wms/index.html', {'client_list': client_list})


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
            post = m.Client.objects.create(
                first_name = first_name, surname = surname, email = email)
            return HttpResponseRedirect(reverse('post_detail', kwargs={
                'post_id': post.id}))
        else:
            form = ClientForm()

    return render(request, 'wms/new_client.html', {
        'form': form,
        })
