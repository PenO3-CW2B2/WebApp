from rest_framework import generics
from rest_framework.views import APIView
from django.core.exceptions import SuspiciousOperation
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.http import HttpResponse, HttpResponseGone
import requests
from django.conf import settings
from bikes import serializers
from bikes.models import Bike, Contract
from bikes.permissions import OwnsBike
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
import pynmea2
import pytz


class UserActivationView(APIView):
    """
    Used to verify an email address
    """

    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        host = request.get_host()
        url = protocol + host + "/" + settings.HOST_PREFIX + "auth/users/activate/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(url, data=post_data)
        if result.status_code == 204:
            return HttpResponse("Accout has been activated succesfully.")
        if result.status_code == 400:
            return HttpResponse("Bad request. Make sure you have copied/enetered the whole URL.")
        if result.status_code == 403:
            return HttpResponse("This account has already been activated.")


class bikeCreateView(generics.CreateAPIView):
    """
    Used to create a new bike
    expected post data:
    - secret = string (requirerd)
    - last_laltitude = float
    - last_longitude = float
    - battery = int
    """
    serializer_class = serializers.BikeSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save()


class bikeDeleteView(generics.DestroyAPIView):
    """
    Used to delete a bike
    """
    serializer_class = serializers.BikeSerializer
    permission_classes = (IsAdminUser,)


class contractCreateView(generics.CreateAPIView):
    """
    Used to create a contract
    expected post data:
    - bike_id = int (requirerd)
    """
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
        serializer.save(user_id=user, bike_id=bike)


class userContracts(APIView):
    """
    Used to get the contracts related to the user
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        contracts = user.contract_set.filter(time_end__isnull=True)
        serializer = serializers.ContractSerializer(contracts, many=True)
        return Response(serializer.data)


class bikeOwnership(APIView):
    """
    Used to create a new ownership for a bike
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, userid, bikeid):
        user = User.objects.get(id=userid)
        bike = Bike.objects.get(id=bikeid)
        bike.owners.add(user)
        serializer = serializers.BikeSerializer(bike)
        return Response(serializer.data)


class userBikeHash(APIView):
    """
    Used to get the hash of the current hirerd bike
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        contracts = user.contract_set.filter(time_end__isnull=True)
        if len(contracts) == 0:
            return HttpResponseGone("No bike hirerd")
        contract = contracts[0]
        serializer = serializers.SecretContractSerializer(contract)
        print(serializer.data)
        return Response(serializer.data)


class bikeList(APIView):
    """
    Used to return a list of all bikes
    """
    permission_classes = (IsAdminUser,)

    def get(self, request):
        bikes = Bike.objects.all()
        serializer = serializers.BikeSerializer(bikes, many=True)
        return Response(serializer.data)


class FreeBikeList(APIView):
    """
    Used to return a list of all unhirerd bikes
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        bikes = Bike.objects.filter(Q(contract__isnull=True) | Q(contract__time_end__isnull=False))
        serializer = serializers.PublicBikeSerializer(bikes, many=True)
        return Response(serializer.data)


class bikeDetails(APIView):
    """
    Used to get or update information of a certain bike
    """
    permission_classes = (OwnsBike,)

    def get(self, request, pk):
        bike = Bike.objects.get(id=pk)
        self.check_object_permissions(request, bike)
        serializer = serializers.BikeSerializer(bike)
        return Response(serializer.data)

    def post(self, request, pk):
        bike = Bike.objects.get(id=pk)
        self.check_object_permissions(request, bike)
        serializer = serializers.BikeSerializer(bike, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class contractList(APIView):
    """
    Used to get a list of all contracts
    """
    permission_classes = (IsAdminUser,)

    def get(self, request):
        contracts = Contract.objects.all()
        serializer = serializers.ContractSerializer(contracts, many=True)
        return Response(serializer.data)


class contractDetails(APIView):
    """
    Used to get information of a specific contract
    """
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        contract = Contract.objects.get(id=pk)
        serializer = serializers.ContractSerializer(contract)
        return Response(serializer.data)


class contractEnd(APIView):
    """
    Used to end a specific contract
    """
    permission_classes = (OwnsBike,)

    def post(self, request, pk):
        contract = Contract.objects.get(id=pk)
        self.check_object_permissions(request, contract.bike)
        if 'timestamp' in request.data:
            end_time = request.data['timestamp']
        else:
            end_time = datetime.datetime.now()
        serializer = serializers.ContractSerializer(contract, data={'time_end': end_time}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class bikeMessage(APIView):
    """
    Used by the bike to send information to the server. Will end any ongoing contracts.
    Expected post data:
    - secret = string
    - gpgga = string
    - battery = int
    - timestamp = int
    """
    permission_classes = (OwnsBike,)

    def post(self, request, pk):
        bike = Bike.objects.get(id=pk)
        self.check_object_permissions(request, bike)
        contracts = bike.contract_set.filter(time_end__isnull=True)
        if len(contracts) != 0:
            contract = contracts[0]
            if 'timestamp' in request.data:
                timestamp = request.data['timestamp']
                end_time = datetime.datetime.fromtimestamp(int(request.data['end_time']), tz=pytz.utc)
            else:
                end_time = datetime.datetime.now()
            serializer = serializers.ContractSerializer(contract, data={'time_end': end_time}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        data = request.data.copy()
        if 'gpgga' in request.data:
            gpgga = request.data['gpgga']
            msg = pynmea2.parse(gpgga)
            if gpgga.gps_qual == 1:
                data.update({'last_longitude': round(msg.longitude, 6), 'last_laltitude': round(msg.latitude, 6)})
        if 'last_laltitude' in data and 'last_longitude' in data:
            if float(data['last_longitude']) == 0.0 and float(data['last_laltitude']) == 0.0:
                del data['last_laltitude']
                del data['last_longitude']
        if 'secret' in data:
            if data['secret'] == '1':
                del data['secret']
        serializer = serializers.BikeSerializer(bike, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
