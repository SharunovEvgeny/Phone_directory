from tkinter import *
from tkinter import messagebox

import requests
from tkinter import *

URL = "http://127.0.0.1:8000/api/"

def createToplevel(x,y,color):
    levelTop = Toplevel(root)
    levelTop.geometry(f'{x}x{y}')
    levelTop['bg'] = f'{color}'
    levelTop.resizable(width=False, height=False)
    # levelTop.grab_set()
    # levelTop.focus_set()
    return levelTop





def deleteContactByNameAndSurname():
    def sendContactDelet():
        response = requests.delete(URL + f"contactDelete/{name.get()}&{surname.get()}")
        if response.status_code==204 or response.status_code==404:
            messagebox.showerror(title="Ошибка", message="Контакта с таким именим и фамилией нет")
        else:
            messagebox.showinfo(title="Успешно",message="Контакт удалён")
            deleteContactBox.destroy()

    deleteContactBox=createToplevel(500,200,"#FFDEAD")
    Label(deleteContactBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    name = Entry(deleteContactBox, width=31, font=40)
    name.grid(row=0, column=1)
    Label(deleteContactBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surname = Entry(deleteContactBox, width=31, font=40)
    surname.grid(row=1, column=1)
    Button(deleteContactBox, text='Удалить', bg='#ADFF2F', command=sendContactDelet).grid(row=34)

def createContacts():
    def sendContact():
        correctNumbers = []
        for number in numbers:
            correctNumber = number['correctNumber'].get()
            if correctNumber == "":
                continue
            number.update({"correctNumber": str(correctNumber)})
            number.update({"category": str(number['category'].get())})
            correctNumbers.append(number)
        response = requests.post(URL + "contactCreate/",
                                 json={"numbers": correctNumbers, "name": name.get(), "surname": surname.get(),
                                       "birthday": birthday.get()})
        createContactsBox.destroy()


    createContactsBox=createToplevel(500,840,"#FFDEAD")
    Label(createContactsBox, text="Введите Имя:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=0, column=0)
    name = Entry(createContactsBox, width=31, font=40)
    name.grid(row=0, column=1)
    Label(createContactsBox, text="Введите Фамилию:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=1, column=0)
    surname = Entry(createContactsBox, width=31, font=40)
    surname.grid(row=1, column=1)
    Label(createContactsBox, text="Введите Дату рождения:", font=40, bg='#FFDEAD', justify=LEFT).grid(row=2, column=0)
    birthday = Entry(createContactsBox, width=31, font=40)
    birthday.grid(row=2, column=1)
    numbers = []
    for count, iter in enumerate(range(0, 28, 2)):
        numberDict = {}
        Label(createContactsBox, text=f"Введите {count + 1} Номер :", font=40, bg='#FFDEAD', justify=LEFT).grid(
            row=iter + 4, column=0)
        number = Entry(createContactsBox, width=31, font=40)
        number.grid(row=iter + 4, column=1)
        Label(createContactsBox, text=f"Введите категорию для {count + 1} Номера :", font=40, bg='#FFDEAD',
              justify=LEFT).grid(row=iter + 5, column=0)
        category = Entry(createContactsBox, width=31, font=40)
        category.grid(row=iter + 5, column=1)
        numberDict.update({"correctNumber": number})
        numberDict.update({"category": category})
        numbers.append(numberDict)
    Button(createContactsBox, text='Создать', bg='#ADFF2F', command=sendContact).grid(row=34)


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


def getAllContacts():
    response = requests.get(URL + "contacts/")

    allContactsBox = Toplevel(root)
    allContactsBox.geometry('600x400')
    allContactsBox.resizable(width=False, height=False)
    canvas = Canvas(allContactsBox, borderwidth=0, bg="#FFC0CB")
    frame = Frame(canvas, background="#FFC0CB")
    vsb = Scrollbar(allContactsBox, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    contacts = response.json()
    print(response.json())

    for count, contact in enumerate(contacts):
        numbers = f""""""
        for number in contact['numbers']:
            numbers += f"""Номер: {str(number['correctNumber'])}\n  Категория: {str(number['category'])}\n\n"""
        Label(frame,
              text=f"""КОНТАКТ НОМЕР {count + 1}\nИмя: {str(contact['name'])}\nФамилия: {str(contact['surname'])}\nДень рождения: {str(contact['birthday'])}\n\n{numbers}""",
              bg='#FFC0CB', font=40).grid(row=count + 1)
    # button = Button(allContactsBox, text='Закрыть', bg='green')
    # button.pack()


root = Tk()

root['bg'] = '#fafafa'

root.title('Телефонный справочник')
root.wm_attributes('-alpha', 0.8)
root.geometry('600x700')
root.resizable(width=False, height=False)

# canvas = Canvas(root, height=600, width=700)
# canvas.pack()

frame = Frame(root, bg='#00FFFF')
frame.place(relwidth=1, relheight=1)

Button(frame, text='Посмотреть все контакты', bg='#FF8C00', command=getAllContacts).pack()
Button(frame, text='Создать контакт', bg='#FF8C00', command=createContacts).pack()
Button(frame,text="Удалить по имени и фамилии",bg='#FF8C00', command=deleteContactByNameAndSurname).pack()

root.mainloop()
