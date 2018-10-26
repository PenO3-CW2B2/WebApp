from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from  bikes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', views.UserActivationView.as_view()),
]
