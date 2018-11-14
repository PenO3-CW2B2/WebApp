from rest_framework import serializers
from bikes.models import Bike, Contract
from django.contrib.auth.models import User
from hashlib import sha256



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

    hash = serializers.SerializerMethodField()

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

    def get_hash(self, obj):
        bike = Bike.objects.get(id=obj.bike_id)
        hash = str(sha256(str(bike.secret).encode() + str(obj.time_start.timestamp()).encode() + str(obj.user_id).encode()).hexdigest())
        return hash

    class Meta:
        model = Contract
        fields = ('hash', 'id', 'user_id', 'bike_id', 'time_start', 'time_end', 'payed')

class SecretContractSerializer(serializers.ModelSerializer):

    hash = serializers.SerializerMethodField()

    def get_hash(self, obj):
        bike = Bike.objects.get(id=obj.bike_id)
        hash = str(sha256(str(bike.secret).encode() + str(obj.time_start.timestamp()).encode() + str(obj.user_id).encode()).hexdigest())
        return hash

    class Meta:
        model = Contract
        fields = ('hash', 'bike_id', 'time_start', 'user_id')
