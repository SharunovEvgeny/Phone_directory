from tkinter import *
from tkinter import messagebox

import requests

from interface.createHelper import *


def soonBirthday():
    response = requests.get(URL + f"contacts/?soon=True")
    sendFilterBox = createToplevel(600, 400, "#FF00FF", root=root)
    frame = createScrollFrame(sendFilterBox, "#FF00FF")
    enterContacts(frame=frame, contacts=response.json())


def searchBirthday():
    def sendSearch():
        if validDayAndMonth(day.get(), month.get()):
            response = requests.get(URL + f"contacts/?day={day.get()}&month={month.get()}")
            if response.status_code != 200 or response.json() == []:
                messagebox.showerror(title="Ошибка", message="Нет таких контактов")
                return
            sendFilterBox = createToplevel(600, 400, "#FF00FF", root=root)
            frame = createScrollFrame(sendFilterBox, "#FF00FF")
            enterContacts(frame=frame, contacts=response.json())
        else:
            return

    searchBox = createToplevel(500, 200, "#FFDEAD", root)
    Label(searchBox, text="Введите месяц:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    month = Entry(searchBox, width=31, font=40)
    month.grid(row=0, column=1)
    Label(searchBox, text="Введите день:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    day = Entry(searchBox, width=31, font=40)
    day.grid(row=1, column=1)
    Button(searchBox, text='Узнать', bg='#ADFF2F', command=sendSearch).grid(row=34)


def differenceBirthday():
    def GT():
        creatorDifferentOrEqualsFunc(params="GT", number=number, URL=URL, root=differenceBirthdayBox)

    def LT():
        creatorDifferentOrEqualsFunc("LT", number=number, URL=URL, root=differenceBirthdayBox)

    def equals():
        creatorDifferentOrEqualsFunc("equals", number=number, URL=URL, root=differenceBirthdayBox)

    differenceBirthdayBox = createToplevel(500, 150, "#FFDEAD", root)
    Label(differenceBirthdayBox, text="Введите количество лет:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0,
                                                                                                           column=0)
    number = Entry(differenceBirthdayBox, width=31, font=40)
    number.grid(row=0, column=1)
    Button(differenceBirthdayBox, text='Больше', bg='#ADFF2F', command=GT).grid(row=1)
    Button(differenceBirthdayBox, text='Меньше', bg='#ADFF2F', command=LT).grid(row=2)
    Button(differenceBirthdayBox, text='Равно', bg='#ADFF2F', command=equals).grid(row=3)


def getAge():
    def sendGetAge():
        response = requests.get(URL + f"contacts/?name={name.get().title()}&surname={surname.get().title()}")
        if response.status_code != 200 or response.json() == []:
            messagebox.showerror(title="Ошибка", message="Контакта с таким именим и фамилией нет")
        else:

            messagebox.showinfo(title="Успешно",
                                message=f"Возраст контакта: {age(str(response.json()[0]['birthday']))}")
            getAgeBox.destroy()

    getAgeBox = createToplevel(500, 200, "#FFDEAD", root)
    Label(getAgeBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    name = Entry(getAgeBox, width=31, font=40)
    name.grid(row=0, column=1)
    Label(getAgeBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surname = Entry(getAgeBox, width=31, font=40)
    surname.grid(row=1, column=1)
    Button(getAgeBox, text='Узнать', bg='#ADFF2F', command=sendGetAge).grid(row=34)


def filterContacts():
    def sendFilterContacts():
        correctNumber = number.get()
        if not validNumberAndBirthday(correctNumber):
            return
        if not validNumberAndBirthday(birthday=birthday.get()):
            return
        if not validData(birthday.get()):
            return
        if re.match(r"\+7\d\d\d\d\d\d\d\d\d\d", str(correctNumber)):
            correctNumber = correctNumber[2:]
            correctNumber = '8' + correctNumber
        requestsText = f"{URL}contacts/?"
        if name.get() != "":
            requestsText += f"name={name.get().title()}&"
        if surname.get() != "":
            requestsText += f"surname={surname.get().title()}&"
        if birthday.get() != "":
            requestsText += f"birthday={birthday.get()}&"
        if number.get() != "":
            requestsText += f"numbers={correctNumber}&"
        response = requests.get(requestsText)
        if response.json() == [] or response.status_code != 200:
            messagebox.showerror(title="Ошибка", message="Нет таких контактов")
        else:
            sendFilterBox = createToplevel(600, 400, "#FF00FF", root=root)
            frame = createScrollFrame(sendFilterBox, "#FF00FF")
            enterContacts(frame=frame, contacts=response.json())

    filterContactsBox = createToplevel(500, 300, "#FFDEAD", root=root)
    Label(filterContactsBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    name = Entry(filterContactsBox, width=31, font=40)
    name.grid(row=0, column=1)
    Label(filterContactsBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surname = Entry(filterContactsBox, width=31, font=40)
    surname.grid(row=1, column=1)
    Label(filterContactsBox, text="Введите Дату рождения:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=2, column=0)
    birthday = Entry(filterContactsBox, width=31, font=40)
    birthday.grid(row=2, column=1)
    Label(filterContactsBox, text="Введите Номер:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=3, column=0)
    number = Entry(filterContactsBox, width=31, font=40)
    number.grid(row=3, column=1)
    Label(filterContactsBox, text="Заполните нужные поля:", font=40, bg='#FFDEAD').grid(row=4, column=0)
    Button(filterContactsBox, text='Отфильтровать', bg='#ADFF2F', command=sendFilterContacts).grid(row=4, column=1)


def deleteContactByNumber():
    def sendContactDelete():
        def sendContacts():
            for count, contact in enumerate(contactsDelete):
                if checkboxs[count].get() == 1:
                    requests.delete(URL + f"contactDelete/{contact}")
            messagebox.showinfo(title="Успешно", message="Контакт удалён")
            deletsBox.destroy()

        if validNumberAndBirthday(correctNumber=number.get()):
            return

        response = requests.get(URL + f"contacts/?numbers={number.get()}")
        if response.status_code == 204 or response.status_code == 404 or response.json() == []:
            messagebox.showerror(title="Ошибка", message="Контакта с таким номером нет")
        else:
            deleteContactBox.destroy()
            deletsBox = createToplevel(700, 700, "#FF00FF", root=root)
            frame = createScrollFrame(deletsBox, "#FF00FF")
            checkboxs, contactsDelete, countRow = chooseContacts(frame=frame, contacts=response.json())
            Button(frame, text='Удалить', bg='#ADFF2F', command=sendContacts).grid(row=countRow + 2)

    deleteContactBox = createToplevel(500, 150, "#FFDEAD", root)
    Label(deleteContactBox, text="Введите Номер:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    number = Entry(deleteContactBox, width=31, font=40)
    number.grid(row=0, column=1)
    Button(deleteContactBox, text='Удалить', bg='#ADFF2F', command=sendContactDelete).grid(row=1)


def deleteContactByNameAndSurname():
    def sendContactDelete():
        response = requests.delete(URL + f"contactDelete/{name.get().title()}&{surname.get().title()}")
        if response.status_code == 204 or response.status_code == 404:
            messagebox.showerror(title="Ошибка", message="Контакта с таким именим и фамилией нет")
        else:
            messagebox.showinfo(title="Успешно", message="Контакт удалён")
            deleteContactBox.destroy()

    deleteContactBox = createToplevel(500, 200, "#FFDEAD", root)
    Label(deleteContactBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    name = Entry(deleteContactBox, width=31, font=40)
    name.grid(row=0, column=1)
    Label(deleteContactBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surname = Entry(deleteContactBox, width=31, font=40)
    surname.grid(row=1, column=1)
    Button(deleteContactBox, text='Удалить', bg='#ADFF2F', command=sendContactDelete).grid(row=34)


def updateContact():
    def sendContactUpdate():
        def sendContact():
            if creatorSendContact(URL=URL, name=name, surname=surname, birthday=birthday, numbers=numbers,
                                  isUpdate=True, updateName=intputName, updateSurname=inputSurname):
                createContactsBox.destroy()

        inputSurname = surnameInst.get()
        intputName = nameInst.get()
        response = requests.get(URL + f"contacts/?name={intputName.title()}&surname={inputSurname.title()}")
        if response.json() != [] or response.status_code != 200:
            updateContactBox.destroy()
            createContactsBox = createToplevel(500, 840, "#FFDEAD", root=root)
            name, surname, birthday, numbers = creatorFieldsForContact(createContactsBox, response=response)
            Button(createContactsBox, text='Обновить', bg='#ADFF2F', command=sendContact).grid(row=34)
        else:
            messagebox.showerror(title="Ошибка", message="Контакта с таким именим и фамилией нет")

    updateContactBox = createToplevel(500, 200, "#FFDEAD", root)
    Label(updateContactBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    nameInst = Entry(updateContactBox, width=31, font=40)
    nameInst.grid(row=0, column=1)
    Label(updateContactBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surnameInst = Entry(updateContactBox, width=31, font=40)
    surnameInst.grid(row=1, column=1)
    Button(updateContactBox, text='Обновить', bg='#ADFF2F', command=sendContactUpdate).grid(row=34)


def createContacts():
    def sendContact():
        if creatorSendContact(URL=URL, name=name, surname=surname, birthday=birthday, numbers=numbers):
            createContactsBox.destroy()
            return

    createContactsBox = createToplevel(500, 840, "#FFDEAD", root=root)
    name, surname, birthday, numbers = creatorFieldsForContact(createContactsBox=createContactsBox)
    Button(createContactsBox, text='Создать', bg='#ADFF2F', command=sendContact).grid(row=34)


def getAllContacts():
    response = requests.get(URL + "contacts/")
    if response.json() == [] or response.status_code != 200:
        messagebox.showerror(title="Ошибка", message="На данный момент в базе данных нет контактов")
    else:
        allContactsBox = createToplevel(600, 400, "#FFC0CB", root=root)
        frame = createScrollFrame(allContactsBox, "#FFC0CB")
        enterContacts(frame=frame, contacts=response.json())


if __name__ == '__main__':
    root = Tk()

    root['bg'] = '#fafafa'
    URL = "http://127.0.0.1:8000/api/"

    root.title('Телефонный справочник')
    root.wm_attributes('-alpha', 0.8)
    root.geometry('600x400')
    root.resizable(width=False, height=False)

    frame = Frame(root, bg='#00FFFF')
    frame.place(relwidth=1, relheight=1)
    (Label(frame, text="Главное Меню", font=100, bg='#00FFFF', justify=LEFT)).pack()
    Button(frame, text='Посмотреть все контакты', bg='#FF8C00', command=getAllContacts).pack()
    Button(frame, text='Создать контакт', bg='#FF8C00', command=createContacts).pack()
    Button(frame, text="Удалить по имени и фамилии", bg='#FF8C00', command=deleteContactByNameAndSurname).pack()
    Button(frame, text="Фильтр контактов", bg='#FF8C00', command=filterContacts).pack()
    Button(frame, text="Узнать сколько лет", bg='#FF8C00', command=getAge).pack()
    Button(frame, text="Изменить контакт", bg='#FF8C00', command=updateContact).pack()
    Button(frame, text="Удалить контакт по номеру", bg='#FF8C00', command=deleteContactByNumber).pack()
    Button(frame, text="Скоро день рождения", bg='#FF8C00', command=soonBirthday).pack()
    Button(frame, text="Узнать контакты по N лет", bg='#FF8C00', command=differenceBirthday).pack()
    Button(frame, text="Поиск по месяцу и дню рождения", bg='#FF8C00', command=searchBirthday).pack()

    root.mainloop()
