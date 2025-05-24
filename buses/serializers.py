from main.models import Bus, LongRouteName, Route
from rest_framework import serializers


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'


class LongRouteNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongRouteName
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'