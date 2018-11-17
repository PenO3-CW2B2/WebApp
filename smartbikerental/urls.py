from django.conf.urls import url, include

urlpatterns = [
    url(r'^auth/', include('bikes.urls')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^auth/', include('djoser.urls.jwt')),
]
