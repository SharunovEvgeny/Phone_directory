from django.db import models


class Number(models.Model):
    correctNumber = models.CharField("Корректный номер", max_length=12)
    category = models.CharField("Категория", max_length=150, default="Отсутствует", null=True, blank=True)


class Contact(models.Model):
    numbers = models.ManyToManyField(Number, related_name="contact_numbers", verbose_name="Номера контакта")
    name = models.CharField("Имя контакта", max_length=150)
    surname = models.CharField("Фамилия контакта", max_length=150)
    birthday = models.DateField("День рождения", null=True, blank=True)
