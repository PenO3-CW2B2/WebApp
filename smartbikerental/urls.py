from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from  bikes import views
from djoser import views as djoserVieuws

urlpatterns = [
    url(r'^auth/', include('bikes.urls')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/', include('djoser.urls.jwt')),
]
