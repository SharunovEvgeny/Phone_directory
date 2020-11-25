import re
import datetime

from django.db.models import Q

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
        contact.surname = contactData['surname']
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


def getSoonContacts():
    day = datetime.date.today().day
    month = datetime.date.today().month
    nextmonth = month + 1
    if month == 12:
        nextmonth = 1
    return Contact.objects.filter(
        Q(birthday__month=month, birthday__day__gte=day) | Q(birthday__month=nextmonth, birthday__day__lte=day))


def getDifferentContacts(GT, LT, equals):
    if GT:
        today = datetime.date.today()
        year = today.year - int(GT)
        nextdata=datetime.date(year-1, today.month, today.day)
        return Contact.objects.filter(birthday__lt=nextdata)
    elif LT:
        today = datetime.date.today()
        year = datetime.date.today().year - int(LT)
        data=datetime.date(year, today.month, today.day)
        return Contact.objects.filter(birthday__gt=data)
    else:
        today = datetime.date.today()
        year = today.year - int(equals)
        data = datetime.date(year, today.month, today.day)
        nextdata = datetime.date(year - 1, today.month, today.day)
        return Contact.objects.exclude(Q(birthday__lt=nextdata)|Q(birthday__gt=data))

def getDayAndMonthFilter(day,month):
    return Contact.objects.filter(birthday__month=int(month),birthday__day=int(day))

