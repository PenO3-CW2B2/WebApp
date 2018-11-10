from rest_framework import serializers
from bikes.models import Bike, Contract
from django.contrib.auth.models import User

class PublicBikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('id', 'modified_date', 'last_longitude', 'last_laltitude')


class BikeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Bike.objects.create(**validated_data)

    class Meta:
        model = Bike
        fields = ('id', 'secret', 'modified_date', 'battery', 'last_longitude', 'last_laltitude')

class ContractSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

    class Meta:
        model = Contract
        fields = ('id', 'user', 'bike', 'time_start', 'time_end', 'payed')
