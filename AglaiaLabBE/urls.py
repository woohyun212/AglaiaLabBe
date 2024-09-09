from django.contrib import admin
from django.urls import path, include
from nadia.urls import urlpatterns as nadia_urls
from thomas.urls import urlpatterns as thomas_urls


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/nadia/', include(nadia_urls)),
    path('api/thomas/', include(thomas_urls)),
]