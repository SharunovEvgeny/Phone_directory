import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Contact
from api.serializer import ContactSerializer, ContactDeleteSerializer
from api.services import getSoonContacts, getDifferentContacts, getDayAndMonthFilter


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self, *args):
        # Задание queryset взависимости от действия
        if self.action == 'update':
            print(*args, flush=True)
            # return Contact.objects.get(name=args, surname=args['surname'])
        else:
            return self.serializer_class

    def get_serializer_class(self):
        # Задание сериализатора взависимости от действия
        if self.action == 'destroy':
            return ContactDeleteSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        # Переопределение метода create для проверки данных
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # Переопределение метода destroy
        try:
            contact = Contact.objects.get(name=kwargs['name'], surname=kwargs['surname'])
            contact.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        try:
            contact = Contact.objects.get(name=kwargs['name'], surname=kwargs['surname'])
            serializer = self.get_serializer(data=request.data, instance=contact)

            serializer.is_valid(raise_exception=True)
            try:
                self.perform_update(serializer)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ContactReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        contacts = self.queryset

        filter_args = {'name': self.request.query_params.get('name'),
                       'surname': self.request.query_params.get('surname'),
                       'birthday': self.request.query_params.get('birthday'),
                       'numbers__correctNumber': self.request.query_params.get('numbers')}
        filter_args = dict((key, value) for key, value in filter_args.items() if value is not None)
        contacts = contacts.filter(**filter_args)
        soon = self.request.query_params.get('soon')
        GT= self.request.query_params.get('GT')
        LT= self.request.query_params.get('LT')
        equals= self.request.query_params.get('equals')
        day = self.request.query_params.get('day')
        month=self.request.query_params.get('month')
        if day and month:
            contacts=getDayAndMonthFilter(day,month)
        if soon=="True":
            contacts=getSoonContacts()
        if GT or LT or equals:
            contacts=getDifferentContacts(GT,LT,equals)
        if contacts:
            return contacts
        else:
            return contacts.none()
