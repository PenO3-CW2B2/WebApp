from django.conf.urls import url
from django.contrib.auth import get_user_model
from bikes import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('bikes', views.UserViewSet)

User = get_user_model()

urlpatterns = [
    url(r'^bikes/create/?$',
        views.bikeCreateView.as_view(),
        name='bike-create'),
    url(r'^bikes/delete/?$',
        views.bikeDeleteView.as_view(),
        name='bike-delete'),
    url(r'contracts/create/?$',
        views.contractCreateView.as_view(),
        name='contract-create'),
    url(r'users/bike/hash/?$',
        views.userBikeHash.as_view(),
        name='user-bike-hash'),
    url(r'^users/contracts/?$',
        views.userContracts.as_view(),
        name='user-contracts'),
    url(r'^users/(?P<userid>[\w-]+)/owns/(?P<bikeid>[\w-]+)?$',
        views.bikeOwnership.as_view(),
        name='bike-ownership'),
    url(r'^bikes/?$',
        views.bikeList.as_view(),
        name='bike-list'),
    url(r'^bikes/(?P<pk>[\w-]+)/?$',
        views.bikeDetails.as_view(),
        name='bike-details'),
    url(r'^freebikes/?$',
        views.FreeBikeList.as_view(),
        name='free-bike-list'),
    url(r'^contracts/?$',
        views.contractList.as_view(),
        name='contract-list'),
    url(r'^contracts/(?P<pk>[\w-]+)/?$',
        views.contractDetails.as_view(),
        name='contract-detials'),
    url(r'^contracts/(?P<pk>[\w-]+)/end/?$',
        views.contractEnd.as_view(),
        name='contract-end'),
    url(r'^activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$',
        views.UserActivationView.as_view(),
        name='user-verify'),
]
