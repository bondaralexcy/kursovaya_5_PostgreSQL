# Курсовая работа № 5 (PostgreSQL)

# Общее описание
В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

Основные шаги проекта
- Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку 
requests
- Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
- Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используйте библиотеку 
psycopg2
- Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
- Создать класс DBManager для работы с данными в БД.

# База данных
База данных имеет две таблицы:
1) companies (компании)
2) vacancies (вакансии)

Отношения между таблицами one-to-many

Связь между таблицами по полю "company_id" (уникальный id компании)

# Класс DBManager
Задание:
Создайте класс DBManager который будет подключаться к БД PostgreSQL и иметь следующие методы:
 
- get_companies_and_vacancies_count()  — получает список всех компаний и количество вакансий у каждой компании.
 
- get_all_vacancies()  — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
 
- get_avg_salary()  — получает среднюю зарплату по вакансиям.
 
- get_vacancies_with_higher_salary()  — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
 
- get_vacancies_with_keyword()  — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

## Термины:
* python, postgres, psycopg2
* requests, sql, pytest
* abc

## Инструкция:

Создайте в PyCharm новый проект, клонировав его из Git
```
git clone git@github.com:bondaralexcy/kursovaya_5_PostgreSQL.git
```
- Создайте виртуальное окружение
```
poetry init
```
- Установите все зависимости из файла 
```
pyproject.toml
```
- Создайте файл `database.ini` - конфигурационный файл с вашими параметрами подключения к БД.
</br>
Пример содержания файла:
```
[postgresql]
host=localhost
user=postgres
password=12345
port=5432
```
В модуле main.py переменной ``db_name`` присвойте наименование новой базы данных

В модуле utils.py модифицируйте список идентификаторов интересующих вас компаний.
Исходный список:
```
companies = [78638,  # Тинькофф
            3529,  # Сбер
            633069,  # Selectel
            1740,  # Яндекс
            2242777,  # Dinord
            2145828,  # ISCO.PRO
            5141773,  # Hammer Systems
            3982116,  # 
            5061718,  # Exemter
            9056230,  # Offer Now
            3203124,  # Sibdev
            914908,  # OneTwoTrip
            1193714  # Southbridge
            ]
```

Запуск проекта осуществляет функция user_interaction()
из модуля main

## Работу выполнил:
Алексей Бондаренко

eMail: bondaralexcy@gmail.com

git: https://github.com/bondaralexcy/