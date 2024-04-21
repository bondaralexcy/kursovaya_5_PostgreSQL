import requests
import psycopg2

# список идентификаторов компаний,
# по которым хотим получить информацию
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

def get_employers():
    """ Запрос к api.hh.ru
    В качестве аргумента принимает список с id компаниями
    Возвращает список словарей вида
    {company:
    vacancies: }
    """
    employers = []
    for company in companies:
        url = f'https://api.hh.ru/employers/{company}'
        company_response = requests.get(url).json()
        vacancy_response = requests.get(company_response['vacancies_url']).json()
        employers.append({
            'company': company_response,
            'vacancies': vacancy_response['items']
        })

    return employers


def clear_string(string: str) -> str:
    """
    Очищает строку от символов из списка symbols
    """

    symbols = ['\n', '<strong>', '\r', '</strong>', '</p>', '<p>', '</li>', '<li>',
               '<b>', '</b>', '<ul>', '<li>', '</li>', '<br />', '</ul>']

    for symbol in symbols:
        string = string.replace(symbol, '')

    return string


def detect_salary(salary):
    """ Определяем уровень зарплаты для вакансии
    """
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            # return round((salary['from'] + salary['to']) / 2)
            return salary['from']
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None


def create_db(database_name, params):
    """ Содаем БД database_name
    """
    connection = psycopg2.connect(database='postgres', **params)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f'DROP DATABASE {database_name}')
        cursor.execute(f'CREATE DATABASE {database_name}')

    connection.close()


def create_tables(database_name, params):
    """ Создаем таблицы
        companies
        vacancies
    """
    connection = psycopg2.connect(database=database_name, **params)

    with connection.cursor() as cursor:
        cursor.execute('CREATE TABLE companies('
                       'company_id serial PRIMARY KEY,'
                       'company_name varchar(50) NOT NULL,'
                       'description text,'
                       'link varchar(200) NOT NULL,'
                       'url_vacancies varchar(200) NOT NULL)')

        cursor.execute('CREATE TABLE vacancies('
                       'vacancy_id serial PRIMARY KEY,'
                       'company_id int REFERENCES companies (company_id) NOT NULL,'
                       'vacancy_title varchar(150) NOT NULL,'
                       'salary int,'
                       'url varchar(200) NOT NULL,'
                       'description text,'
                       'experience varchar(70))')

    connection.commit()
    connection.close()


def fill_db(employers, database_name, params):
    """ Заполняем таблицы БД данными с сайта компании hh.ru
    @param employers:   список словарей вида  {company: vacancies: }
    @param database_name: наименование БД
    @param params: парметры подключения к БД
    """
    connection = psycopg2.connect(database=database_name, **params)

    with connection.cursor() as cursor:
        for employer in employers:
            # Заполняем запись в таблице companies
            cursor.execute('INSERT INTO companies (company_name, description, link, url_vacancies)'
                           'VALUES (%s, %s, %s, %s)'
                           'returning company_id',
                           (employer["company"].get("name"),
                            clear_string(employer["company"].get("description")),
                            employer["company"].get("alternate_url"),
                            employer["company"].get("vacancies_url")))

            company_id = cursor.fetchone()[0]
            # Заполняем записи в таблице vacancies
            # для данной компании (связь между таблицами по company_id)
            for vacancy in employer["vacancies"]:
                salary = detect_salary(vacancy["salary"])
                cursor.execute('INSERT INTO vacancies'
                               '(company_id, vacancy_title, salary, url, description, experience)'
                               'VALUES (%s, %s, %s, %s, %s, %s)',
                               (company_id, vacancy["name"], salary,
                                vacancy["alternate_url"], vacancy["snippet"].get("responsibility"),
                                vacancy["experience"].get("name")))

    connection.commit()
    connection.close()

def pretty_print(vc_list):
    """ Отладочная печать"""
    i = 0
    for unit in vc_list:
        i += 1
        print(unit)