from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include('nadia.urls'))
]



