from rest_framework import serializers

from api.models import Contact, Number


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
                correctNumber, isCreate = Number.objects.get_or_create(correctNumber=dict(number)['correctNumber'])
                contact.numbers.add(correctNumber)
        return contact


class ContactDeleteSerializer(serializers.ModelSerializer):
    # Сериализатор для удаления по имени и фамилии
    class Meta:
        model = Contact
        fields = ("name", "surname")
