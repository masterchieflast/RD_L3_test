from datetime import date

from rest_framework import serializers
from .models import NetworkObject, Product, Contact


class NetworkObjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = NetworkObject
        fields = '__all__'
        read_only_fields = ('debt', 'level', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=25)
    release_date = serializers.DateField()

    def validate_release_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата выхода на рынок не может быть в будущем.")
        return value

    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'