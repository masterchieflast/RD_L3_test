from rest_framework import serializers
from .models import NetworkObject, Product


class NetworkObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkObject
        fields = '__all__'
        read_only_fields = ('debt', 'level', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
