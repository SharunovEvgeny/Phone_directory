import re
from tkinter import Canvas, Frame, Scrollbar, Toplevel, Label, messagebox, Entry, LEFT, Checkbutton, IntVar
import datetime

import requests


def creatorSendContact(URL, name, surname, birthday, numbers, isUpdate=False, updateName=None, updateSurname=None):
    correctNumbers = []
    if name.get() == "" or surname.get() == "":
        messagebox.showerror(title="Ошибка", message="Имя и фамилия не должны быть пустыми")
        return False

    if not isUpdate:
        responce = requests.get(URL + f"contacts/?name={name.get().title()}&surname={surname.get().title()}")
        if responce.json() != []:
            messagebox.showerror(title="Ошибка", message="Контакт с таким именим и фамилией уже существует")
            return False
    if not validNumberAndBirthday(birthday=birthday.get()):
        return False

    for number in numbers:
        try:
            correctNumber = number['correctNumber'].get()
        except:
            correctNumber = number['correctNumber']
        if correctNumber == '':
            continue
        if not validNumberAndBirthday(correctNumber=correctNumber):
            return False
        number.update({"correctNumber": correctNumber})
        try:
            correctCategory = number['category'].get()
        except:
            correctCategory = number['category']
        if correctCategory == '':
            number.update({"category": "Отсутствует"})
        else:
            number.update({"category": correctCategory})
        correctNumbers.append(number)
    if correctNumbers == []:
        messagebox.showerror(title="Ошибка", message="Добавьте хотябы один контакт")
        return False

    correctBirthday = birthday.get()
    if correctBirthday == "":
        correctBirthday = None
    else:
        if not validData(correctBirthday):
            return False
    if not isUpdate:
        response = requests.post(URL + "contactCreate/",
                                 json={"numbers": correctNumbers, "name": name.get().title(),
                                       "surname": surname.get().title(),
                                       "birthday": correctBirthday})
    else:
        response = requests.put(URL + f"contactUpdate/{str(updateName).title()}&{str(updateSurname).title()}/",
                                json={"numbers": correctNumbers, "name": name.get().title(),
                                      "surname": surname.get().title(),
                                      "birthday": correctBirthday})

    if response.status_code != 201 and response.status_code != 200:
        messagebox.showerror(title="Ошибка",
                             message="Не верный формат даты дня рождения введите существующую дату в формате:\nГГГГ-ММ-ДД")
        return False
    else:
        if isUpdate:
            messagebox.showinfo(title="Успешно", message="Контакт обновлён")
        else:
            messagebox.showinfo(title="Успешно", message="Контакт создан")
        return True


def creatorFieldsForContact(createContactsBox, response=None):
    Label(createContactsBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    name = Entry(createContactsBox, width=31, font=40)
    name.grid(row=0, column=1)
    try:
        name.insert(0, str(response.json()[0]['name']))
    except:
        pass
    Label(createContactsBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surname = Entry(createContactsBox, width=31, font=40)
    surname.grid(row=1, column=1)
    try:
        surname.insert(0, str(response.json()[0]['surname']))
    except:
        pass
    Label(createContactsBox, text="Введите Дату рождения:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=2,
                                                                                                      column=0)
    birthday = Entry(createContactsBox, width=31, font=40)
    birthday.grid(row=2, column=1)
    try:
        birthday.insert(0, str(response.json()[0]['birthday']))
    except:
        pass
    numbers = []
    for count, iter in enumerate(range(0, 22, 2)):
        numberDict = {}
        Label(createContactsBox, text=f"Введите {count + 1} Номер :", font=40, bg='#FFDEAD', justify=LEFT).grid(
            row=iter + 4, column=0)
        number = Entry(createContactsBox, width=31, font=40)
        number.grid(row=iter + 4, column=1)
        try:
            number.insert(0, str(response.json()[0]['numbers'][count]['correctNumber']))
        except:
            pass
        Label(createContactsBox, text=f"Введите категорию для {count + 1} Номера :", font=40, bg='#FFDEAD',
              justify=LEFT).grid(row=iter + 5, column=0)
        category = Entry(createContactsBox, width=31, font=40)
        category.grid(row=iter + 5, column=1)
        try:
            category.insert(0, str(response.json()[0]['numbers'][count]['category']))
        except:
            pass
        numberDict.update({"correctNumber": number})
        numberDict.update({"category": category})
        numbers.append(numberDict)
    return name, surname, birthday, numbers


def validNAge(diffrentAge):
    if not (re.fullmatch(r'\d\d', diffrentAge) or re.fullmatch(r'\d', diffrentAge)):
        messagebox.showerror(title="Ошибка",
                             message="Не верный формат количетсва лет\nВведите двухзначное или однозначное число")
    return False


def age(birthday):
    today = datetime.date.today()
    birthday = birthday.split('-')
    birthdayAr = datetime.date(int(birthday[0]), int(birthday[1]), int(birthday[2]))
    days = (today - birthdayAr).days
    years, days = divmod(days, 365.2425)
    months, days = divmod(days, 365.2425 / 12.0)
    return f"\nЛет: {int(years)}\nМесяцев: {int(months)}\nДней: {int(days)}"


def validDayAndMonth(day, month):
    try:
        datetime.date(int(2000), int(str(month)), int(str(day)))
    except:
        messagebox.showerror(title="Ошибка", message="Неверно введён месяц или день")
        return False

    return True


def validData(birthday):
    if birthday > str(datetime.date.today()):
        messagebox.showerror(title="Ошибка", message="Дата больше сегодняшней")
        return False
    return True


def validNumberAndBirthday(correctNumber=None, birthday=None):
    if correctNumber == "":
        return True
    if correctNumber is not None and not (
            re.fullmatch(r'8\d\d\d\d\d\d\d\d\d\d', correctNumber) or re.fullmatch(r'\+7\d\d\d\d\d\d\d\d\d\d',
                                                                                  correctNumber)):
        messagebox.showerror(title="Ошибка",
                             message="Не верный формат номера телефона введите +7 или 8 и ещё 10 цифр подряд")
        return False
    if birthday == "":
        return True
    if birthday is not None and not re.fullmatch(r'\d\d\d\d-\d\d-\d\d', birthday):
        messagebox.showerror(title="Ошибка", message="Не верный формат даты дня рождения введите ГГГГ-ММ-ДД")
        return False
    return True


def createToplevel(x, y, color, root):
    levelTop = Toplevel(root)
    levelTop.geometry(f'{x}x{y}')
    levelTop['bg'] = f'{color}'
    levelTop.resizable(width=False, height=False)
    levelTop.grab_set()
    levelTop.focus_set()
    return levelTop


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


def createScrollFrame(levelTop, color):
    canvas = Canvas(levelTop, borderwidth=0, bg="#FFC0CB")
    frame = Frame(canvas, background="#FFC0CB")
    vsb = Scrollbar(levelTop, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    return frame


def enterContacts(frame, contacts):
    for count, contact in enumerate(contacts):
        numbers = f""""""
        for number in contact['numbers']:
            numbers += f"""Номер: {str(number['correctNumber'])}\n  Категория: {str(number['category'])}\n\n"""
        correctBirthday = contact['birthday']
        if correctBirthday is None:
            correctBirthday = "Не указан"
        Label(frame,
              text=f"""КОНТАКТ НОМЕР {count + 1}\nИмя: {str(contact['name']).title()}\nФамилия: {str(contact['surname']).title()}\nДень рождения: {str(correctBirthday)}\n\n{numbers}""",
              bg='#FFC0CB', font=40).grid(row=count + 1)


def chooseContacts(frame, contacts):
    checkboxs = []
    contactsDelete = []
    count = 0
    for count, contact in enumerate(contacts):
        checkboxs.append(IntVar())
        contactsDelete.append(f"{str(contact['name']).title()}&{str(contact['surname']).title()}")
        Label(frame,
              text=f"""КОНТАКТ НОМЕР {count + 1}\nИмя: {str(contact['name']).title()}\nФамилия: {str(contact['surname']).title()}\n\n""",
              bg='#FFC0CB', font=40).grid(row=count + 1, column=0)
        Checkbutton(frame, text="Удалить", variable=checkboxs[count], onvalue=1, offvalue=0).grid(row=count + 1,
                                                                                                  column=1)
    return checkboxs, contactsDelete, count


def creatorDifferentOrEqualsFunc(params, number, URL, root):
    if validNAge(number.get()):
        return
    response = requests.get(URL + f"contacts/?{params}={number.get()}")
    if response.status_code != 200 or response.json() == []:
        messagebox.showerror(title="Ошибка", message="Нет таких контактов")
        return
    sendFilterBox = createToplevel(600, 400, "#FF00FF", root=root)
    frame = createScrollFrame(sendFilterBox, "#FF00FF")
    enterContacts(frame=frame, contacts=response.json())
