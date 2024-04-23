import os
from src.utils import get_employers, create_db, create_tables, fill_db, pretty_print
from config import config
from classes.db_manager import DBManager
db_name = 'db_kurs_work_5'

def fill_postgres_db():
    """ Получаем данные от сервиса api.hh.ru и
        заполняем таблицы базы данных database_name
    """
    params = config()
    data = []

    # Создаем БД database_name
    create_db(db_name, params)

    # Создаем в БД таблицы "companies" и "vacancies"
    create_tables(db_name, params)

    # Получаем список словарей data[] - данные от сервиса api.hh.ru
    data = get_employers()

    # Заполняем таблицы БД данными с сайта компании hh.ru
    fill_db(data, db_name, params)

    print(f"Ответ от hh.ru получен и записан в БД '{db_name}'")


def try_dbmanager():
    """ Пример использования методов класса DBManager"""
    parameters = config()
    db_manager = DBManager(db_name, parameters)

    # for company in db_manager.get_all_companies_in_request():
    #     print(f"{company}")
    # exit(0)

    while True:
        what_to_do = input("\n\nВыбрать режим работы с классом DBManager:\n"
                           "1 - Cписок всех компаний и количество вакансий у каждой компании\n"
                           "2 - Cписок всех вакансий с указанием названий компании, вакансии и зарплаты и ссылки на вакансию\n"
                           "3 - Cредняя зарплата по вакансиям\n"
                           "4 - Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
                           "5 - Cписок всех вакансий, в названии которых содержатся ереданные в метод слова\n"
                           "0 - Выход из программы\n>")

        if what_to_do == '1':
            any_char = input("\n Cписок всех компаний и количество вакансий у каждой компании (Enter)")
            print("К О М П А Н И И")
            for idx, company in enumerate(db_manager.get_companies_and_vacancies_count(), start=1):
                print(f"{idx}. {company[0]} - вакансий - {company[1]}")

        elif what_to_do == '2':
            any_char = input(
                "\n Cписок всех вакансий с указанием названий компании, вакансии и зарплаты и ссылки на вакансию (Enter)")
            print("В А К А Н С И И")
            for idx, item in enumerate(db_manager.get_all_vacancies(), start=1):
                print(f"{idx}. {item[1]} - {item[0]} - Зарплата: {item[2] or 'нет данных'} - {item[3]}")

        elif what_to_do == '3':
            any_char = input("\n Cредняя зарплата по вакансиям (Enter)")
            print("Компания  --  Зарплата")
            for idx, company in enumerate(db_manager.get_avg_salary(), start=1):
                print(f"{idx}. {company[0]} -- {company[1]}")

        elif what_to_do == '4':
            any_char = input("\n Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям (Enter)")
            print("В А К А Н С И И")
            pretty_print(db_manager.get_vacancies_with_higher_salary())

        elif what_to_do == '5':
            # Фильтрация вакансий по ключевым словам
            filter_words = input("Введите ключевые слова через запятую (по умолчанию - python,sql): ").lower().split(
                ',')
            if filter_words == ['']:
                filter_words = ['python', 'sql']
            print(f"\n 5 Cписок всех вакансий, в названии которых содержатся слова: {filter_words}")
            pretty_print(db_manager.get_vacancies_with_keyword(filter_words))

        elif what_to_do == '0':
            print("\n Работа завершена!")
            exit(0)
        else:
            os.system('clear')
        #     print("\n Работа завершена!")
        #     exit(0)




def user_interaction():
    what_to_do = input("Выберите, что делаем: \n"
                       "1 - Запрос к hh.ru и заполнение БД\n"
                       "2 - Запросы к PostgreSQL\n"
                       "0 - Выход из программы\n>")

    if what_to_do == '1':
        fill_postgres_db()
    elif what_to_do == '2':
        try_dbmanager()
    elif what_to_do == '0':
        print("Работа завершена!")
        exit(0)
    else:
        print("Работа завершена!")
        exit(0)


if __name__ == '__main__':
    user_interaction()
