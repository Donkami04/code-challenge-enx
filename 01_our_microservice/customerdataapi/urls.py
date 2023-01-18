# -*- coding: utf-8 -*-
"""
URLs for customerdataapi.
"""
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from customerdataapi.views import CustomerDataViewSet

from . import views

ROUTER = DefaultRouter()
ROUTER.register(r'customerdata', CustomerDataViewSet)

app_name = 'customerdataapi'

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/v1/', include(ROUTER.urls)),
    path(r'', TemplateView.as_view(template_name="customerdataapi/base.html")),
    path(r'modifylevel/', views.upgradeInterface, name='modify_interface'),
    path(r'modifylevel/<int:id>', views.upgradeLevel, name='modify_level'),
    path(r'succes/', views.upgradeLevel, name='modify_level2'),
]
