from django.contrib.admin.utils import lookup_field
from django.shortcuts import render

# Create your views here.

# user view set  ###########
from rest_framework import viewsets
from .serializers import *


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


######################################
from rest_framework import viewsets, status
from rest_framework.response import Response

import requests
from bser_api import BserAPI
from AglaiaLabBE.settings.base import ER_API_KEY

# BserAPI Instance
er_api = BserAPI(ER_API_KEY)
CURRENT_SEASON = 25
