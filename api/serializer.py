from rest_framework import serializers, status
from rest_framework.response import Response

from api.models import Contact, Number
import re


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
        numbers = validated_data.pop('numbers')


        contactData = dict(validated_data)
        # Проверка на существование контакта с таким именим и фамилией
        contact, isCreate = Contact.objects.get_or_create(name=contactData['name'], surname=contactData['surname'])
        if isCreate:
            contact.birthday = contactData['birthday']
            contact.save()
            # Создание(в случае существования беруться старые) номеров и добавление их к текущему контакту
            for number in numbers:
                strNumber=dict(number)['correctNumber']
                if re.match(r'8\d\d\d\d\d\d\d\d\d\d', strNumber) or re.match(r"\+7\d\d\d\d\d\d\d\d\d\d", strNumber):
                    if strNumber[0]=='+':
                        strNumber='8'+strNumber[2:]
                    correctNumber, isCreate = Number.objects.get_or_create(correctNumber=strNumber)
                    correctNumber.category=dict(number)['category']
                    correctNumber.save()
                    contact.numbers.add(correctNumber)
                else:
                    contact.delete()
                    raise ValueError('Phone number error')
        return contact


class ContactDeleteSerializer(serializers.ModelSerializer):
    # Сериализатор для удаления по имени и фамилии
    class Meta:
        model = Contact
        fields = ("name", "surname")
