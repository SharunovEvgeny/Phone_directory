from django.db.migrations import serializer
from django.http import Http404
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Contact
from api.serializer import ContactSerializer, ContactDeleteSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_serializer_class(self):
        # Задание сериализатора взависимости от действия
        if self.action == 'destroy':
            return ContactDeleteSerializer
        else:
            return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        # Переопределение метода destroy
        try:
            contact = Contact.objects.get(name=kwargs['name'], surname=kwargs['surname'])
            contact.delete()
            return Response(status=status.HTTP_200_OK)
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
                       'numbers__correctNumber':self.request.query_params.get('numbers')}
        filter_args = dict((key, value) for key, value in filter_args.items() if value is not None)
        contacts = contacts.filter(**filter_args)
        if contacts:
            return contacts
        else:
            return contacts.none()