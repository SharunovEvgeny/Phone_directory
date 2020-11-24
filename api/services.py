import re

from api.models import Contact, Number


def createOrUpdateContacts(validated_data, update=True, instance=None):
    isCreate = True
    numbers = validated_data.pop('numbers')
    contactData = dict(validated_data)
    # Проверка на существование контакта с таким именим и фамилией
    if update:
        contact = Contact.objects.get(name=instance.name, surname=instance.surname)
    else:
        contact, isCreate = Contact.objects.get_or_create(name=contactData['name'], surname=contactData['surname'])
    if isCreate or update:
        contact.birthday = contactData['birthday']
        contact.name = contactData['name']
        contact.surname=contactData['surname']
        if numbers != []:
            contact.numbers.clear()
        contact.save()
        # Создание(в случае существования беруться старые) номеров и добавление их к текущему контакту
        for number in numbers:
            strNumber = dict(number)['correctNumber']
            if re.fullmatch(r'8\d\d\d\d\d\d\d\d\d\d', strNumber) or re.fullmatch(r"\+7\d\d\d\d\d\d\d\d\d\d", strNumber):
                if strNumber[0] == '+':
                    strNumber = '8' + strNumber[2:]
                correctNumber, isCreate = Number.objects.get_or_create(correctNumber=strNumber)
                correctNumber.category = dict(number)['category']
                correctNumber.save()
                contact.numbers.add(correctNumber)
            else:
                contact.delete()
                raise ValueError('Phone number error')
    else:
        raise ValueError('Контакт уже есть')
    return contact
