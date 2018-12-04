from rest_framework import serializers
from bikes.models import Bike, Contract
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from hashlib import sha256


def calculateContractHash(contract):
    bike = Bike.objects.get(id=contract.bike_id)
    hash = str(sha256((str(bike.secret) + str(int(contract.time_start.timestamp())) + str(contract.user.username)).encode()).hexdigest())
    return hash


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = DjoserUserCreateSerializer.Meta.fields + ('first_name', 'last_name')


class PublicBikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('id', 'modified_date', 'last_longitude', 'last_laltitude')


class BikeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Bike.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.secret = validated_data.get('secret', instance.secret)
        instance.battery = validated_data.get('battery', instance.battery)
        instance.last_longitude = validated_data.get('last_longitude', instance.last_longitude)
        instance.last_laltitude = validated_data.get('last_laltitude', instance.last_laltitude)
        instance.save()
        return instance

    class Meta:
        model = Bike
        fields = ('id', 'secret', 'modified_date', 'battery', 'last_longitude', 'last_laltitude')


class ContractSerializer(serializers.ModelSerializer):

    hash = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    def create(self, validated_data):
        return Contract.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.save()
        return instance

    def get_hash(self, obj):
        calculateContractHash(obj)

    def get_timestamp(self, obj):
        return int(obj.time_start.timestamp())

    class Meta:
        model = Contract
        fields = ('timestamp', 'hash', 'id', 'user_id', 'bike_id', 'time_start', 'time_end', 'payed')


class SecretContractSerializer(serializers.ModelSerializer):

    hash = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    def get_hash(self, obj):
        calculateContractHash(obj)

    def get_timestamp(self, obj):
        return int(obj.time_start.timestamp())

    class Meta:
        model = Contract
        fields = ('timestamp', 'hash', 'bike_id', 'time_start', 'user_id')
