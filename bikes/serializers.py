from rest_framework import serializers
from bikes.models import Bike, Contract
from django.contrib.auth.models import User

class BikeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Bike.objects.create(**validated_data)

    class Meta:
        model = Bike
        fields = ('secret', 'modified_date', 'battery', 'last_longitude', 'last_laltitude')

class ContractSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

    class Meta:
        model = Contract
        fields = ('user', 'bike', 'time_start', 'time_end', 'payed')
