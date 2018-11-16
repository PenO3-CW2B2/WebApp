from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from django.core.exceptions import SuspiciousOperation
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.http import HttpResponse
import requests
from django.conf import settings
from bikes import serializers, signals
from bikes.models import Bike, Contract
import datetime
from django.db.models import Q

class UserActivationView(APIView):
    """
    Used to verify an email address
    """
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        host = request.get_host()
        url = protocol + host + "/" + settings.HOST_PREFIX + "auth/users/activate/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(url, data = post_data)
        if result.status_code == 204:
            return HttpResponse("Accout has been activated succesfully.")
        if result.status_code == 400:
            return HttpResponse("Bad request. Make sure you have copied/enetered the whole URL.")
        if result.status_code == 403:
            return HttpResponse("This account has already been activated.")

class bikeCreateView(generics.CreateAPIView):
    serializer_class = serializers.BikeSerializer
    permission_classes = (IsAdminUser,)
    def perform_create(self, serializer):
        data = self.request.data
        serializer.save()

class bikeDeleteView(generics.DestroyAPIView):
    serializer_class = serializers.BikeSerializer
    permission_classes = (IsAdminUser,)

class contractCreateView(generics.CreateAPIView):
    serializer_class = serializers.ContractSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        print(self.request.user.contract_set.filter(time_end__isnull=True))
        if self.request.user.contract_set.filter(time_end__isnull=True):
            raise SuspiciousOperation("Invalid request; you already hire a bike")
        bike = self.request.data['bike_id']
        if Bike.objects.get(id=bike).contract_set.filter(time_end__isnull=True):
            raise SuspiciousOperation("Invalid request; this bike is already hirerd")
        user = self.request.user.id
        contract = serializer.save(user_id=user, bike_id=bike)

class userContracts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        contracts = user.contract_set.filter(time_end__isnull=True)
        serializer = serializers.ContractSerializer(contracts, many=True)
        return Repsone(serializer.data)

class userBikeHash(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        contracts = user.contract_set.filter(time_end__isnull=True)
        contract = contracts[0]
        bike = Bike.objects.get(id=contract.bike_id)
        hash = calculateBikeHash(bike.secret, contract.time_start, user.id)
        serializer = serializers.SecretContractSerializer(contract, context={'hash': hash})
        print(serializer.data)
        return Response(serializer.data)

class bikeList(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = serializers.BikeSerializer(bikes, many=True)
        return Response(serializer.data)

class FreeBikeList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        bikes = Bike.objects.filter(Q(contract__isnull = True) | Q(contract__time_end__isnull = False))
        serializer = serializers.PublicBikeSerializer(bikes, many=True)
        return Response(serializer.data)


class bikeDetails(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        bike = Bike.objects.get(id=pk)
        serializer = serializers.BikeSerializer(bike)
        return Response(serializer.data)

class contractList(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = serializers.ContractSerializer(contracts, many=True)
        return Response(serializer.data)

class contractDetails(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        serializer = serializers.ContractSerializer(contract)
        return Response(serializer.data)
