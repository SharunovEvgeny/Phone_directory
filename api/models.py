from django.db import models


class Number(models.Model):
    correctNumber = models.CharField("Корректный номер", max_length=11)
    category = models.CharField("Категория",max_length=150,null=True)


class Contact(models.Model):
    numbers = models.ManyToManyField(Number, related_name="contact_numbers", verbose_name="Номера контакта")
    name = models.CharField("Имя контакта", max_length=150)
    surname = models.CharField("Фамилия контакта", max_length=150)
    birthday = models.DateField("День рождения", null=True, blank=True)
# class Message(models.Model):
#     chat =models.ForeignKey(Chat,on_delete=models.CASCADE,verbose_name="Сообщения в этом чате")
#     text=models.TextField("Текст сообщения", null=True, blank=True)
#     data = models.DateTimeField("Время отправки", null=True, blank=True)
#     user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Сообщения этого пользователя")


# class UserInformation(models.Model):
#     user = models.OneToOneField(User,related_name="user_info", on_delete=models.CASCADE)
#     name = models.CharField(max_length=100,null=True, blank=True)
#     surname = models.CharField(max_length=100,null=True, blank=True)
#     birthdate = models.CharField(max_length=100,null=True, blank=True)
