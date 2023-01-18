# -*- coding: utf-8 -*-
"""
Views for customerdataapi.
"""
from __future__ import absolute_import, unicode_literals

from rest_framework import viewsets, permissions

from customerdataapi.models import CustomerData
from customerdataapi.serializers import CustomerDataSerializer

from django.shortcuts import render
from django.http import HttpResponse

from .forms import ChangeSubscription


class CustomerDataViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving CustomerData.
    """

    queryset = CustomerData.objects.all()
    serializer_class = CustomerDataSerializer
    permission_classes = (permissions.AllowAny,)

def upgradeInterface(request):
    customers = CustomerData.objects.all()
    return render(request, 'customerdataapi/modify_interface.html', {'customers_list': customers})

    
def upgradeLevel(request):    
    if request.method == 'POST':
        id = request.POST['id']
        newSubscription = request.POST['subscription']
        customer = CustomerData.objects.get(id=id)
        customer.data['SUBSCRIPTION'] = newSubscription
        customer.save()
        return HttpResponse("Succes")
    else:
        return HttpResponse("Fallo")
        
    
    
        
        
        