from rest_framework import serializers, status
from rest_framework.response import Response

from api.models import Contact, Number
import re

from api.services import createOrUpdateContacts


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        exclude = ("id",)


class ContactSerializer(serializers.ModelSerializer):
    #Сереиализатор для создания и вывода контакта
    numbers = NumberSerializer(many=True, required=False)

    class Meta:
        model = Contact
        exclude = ("id",)

    def create(self, validated_data):
        # Переопределение метода create
        return createOrUpdateContacts(validated_data,update=False)


    def update(self, instance, validated_data):
        return createOrUpdateContacts(validated_data=validated_data,update=True,instance=instance)


class ContactDeleteSerializer(serializers.ModelSerializer):
    # Сериализатор для удаления по имени и фамилии
    class Meta:
        model = Contact
        fields = ("name", "surname")
