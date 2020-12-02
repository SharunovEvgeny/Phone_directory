# Phone_directory
Для запуска проекта откройте терминал  и перейдя в папку с проектом выполните эти команды(если не работает замените
pip на pip3 и python на python3):
## Для запуска проекта откройте терминал  и перейдя в папку с проектом выполните эти команды:
- `pip install -r requirements.txt`
- `python manage.py runserver`
## После этого у вас запуститьтся сервер. Откройте новый терминал в папке с проектом и напишите:
- `python start.py
## Какие есть функции?
- Просмотр всех контактов
- Создание контакта
- Удаление по имени и фамилии
- Удаление по номеру одного или несколько контактов
- Фильтр контактов по одному или нескольким полям
- Изменение контактов по имени и фамилии, с возможностью поменять любое поле
- Узнать возраст контакта
- Узнать у кого день рождения в ближайшие 30 дней
- Узнать контакты, которым N лет или они старше или младше N лет
- Поиск контактов по месяцу и дню рождения.
## Ссылка на подробный видеоурок, как пользоваться моим приложением. Ролик на ютубе.
- https://youtu.be/sQ5It-6sazg
## Где данные?
- Все данные хранятся, в файле db.sqlite3
## Как сделан интерфейс?
- Весь интерфейс реализован с помощью библиотеки tkinter, которая включена в стандартный python
- С помошью библиотеки requests, посылаются запросы на сервер
## Как сделан сервер?
- Сервер создан с помошью Django и Django-rest-framework.
- API реализован с использованием viewsets
- Созданы две модели Сontact и Number с отношением ManyToMany

