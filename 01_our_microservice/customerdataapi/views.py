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
from django.utils import timezone


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
        print("XXXXXXXXX METODO POST ", request.POST)
        id = request.POST['id']
        newSubs = request.POST['subscription']
        
        customer = CustomerData.objects.get(id=id)
        currentSubs = customer.data['SUBSCRIPTION']
        
        if currentSubs == 'premium' and newSubs == 'free' or newSubs == 'basic':
            customer.data['DOWNGRADE_DATE'] = timezone.now()
            
        elif currentSubs == 'free' and newSubs == 'basic' or newSubs == 'premium':
            customer.data['UPGRADE_DATE'] = timezone.now()
            
        elif currentSubs == 'basic' and newSubs == 'free':
            customer.data['DOWNGRADE_DATE'] = timezone.now()
            
        elif currentSubs == 'basic' and newSubs == 'premium':
            customer.data['UPGRADE_DATE'] = timezone.now()
            
        elif currentSubs == newSubs:
            return HttpResponse(f"The user already has the Subscription {newSubs}")
            
        customer.data['SUBSCRIPTION'] = newSubs         
        customer.save()
        
        
        return HttpResponse("Succes")
    else:
        return HttpResponse("Fallo")
    
# def features(id):
    
#     customer = CustomerData.objects.get(id=id)
#     customer.data['UPGRADE_DATE'] = timezone.now()
#     return customer.save()
        
    
    
        
        
        