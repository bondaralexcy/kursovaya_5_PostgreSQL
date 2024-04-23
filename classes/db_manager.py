from abc import ABC, abstractmethod
import psycopg2
from config import config

class PGSManager(ABC):
    """
    Абстракный класс для работы с БД
    """
    @abstractmethod
    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        pass

    @abstractmethod
    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

    @abstractmethod
    def get_vacancies_with_keyword(self, word_list: list):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        pass


class DBManager(PGSManager):
    """ Класс DBManager дает возможность подключаться к БД PostgreSQL
        Методы класса реализуют ряд запросов к ДБ
    """
    def __init__(self, database_name, params=config()):
        self.database_name = database_name
        self.params = params
        self.check_db()

    def check_db(self):
        """
        Проверим существование базы данных.
        Если ее нет, то создаем.
        """
        try:
            with psycopg2.connect(database=self.database_name, **self.params) as conn:
            # with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute("SELECT * FROM companies")
                        cur.execute("SELECT * FROM vacancies")
                    except Exception as exp_no_tab:
                        print(f'{exp_no_tab} В базе данных отсутствуют рабочие таблицы')
                        exit(1)

            conn.close()
        except Exception as exp:
            print(f'{exp} Надо создать базу данных "{self.database_name}"')
            exit(1)
        else:
            print(f'База данных {self.database_name} существует. Продолжаем работу.')


    def get_companies_and_vacancies_count(self):
        """ Метод получает список всех компаний и количество вакансий у каждой компании
        """
        try:
            connection = psycopg2.connect(database=self.database_name, **self.params)
            with connection.cursor() as cursor:
                cursor.execute('SELECT company_name, COUNT(vacancy_id) '
                               'FROM companies '
                               'JOIN vacancies USING (company_id) '
                               'GROUP BY company_name;')

                data = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        connection.close()
        return data

    def get_all_vacancies(self):
        """ Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        try:
            connection = psycopg2.connect(database=self.database_name, **self.params)
            with connection.cursor() as cursor:
                cursor.execute('SELECT vacancy_title, company_name, salary, vacancies.url '
                               'FROM vacancies '
                               'JOIN companies USING (company_id);')

                data = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        connection.close()
        return data

    def get_avg_salary(self):
        """ Метод получает среднюю зарплату по вакансиям
        """
        try:
            connection = psycopg2.connect(database=self.database_name, **self.params)
            with connection.cursor() as cursor:
                cursor.execute('SELECT company_name, round(AVG(salary)) AS average_salary '
                               'FROM companies '
                               'JOIN vacancies USING (company_id) '
                               'GROUP BY company_name;')

                data = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        connection.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """ Метод получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        """
        try:
            connection = psycopg2.connect(database=self.database_name, **self.params)
            with connection.cursor() as cursor:
                cursor.execute('SELECT * '
                               'FROM vacancies '
                               'WHERE salary > (SELECT AVG(salary) FROM vacancies);')

                data = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        connection.close()
        return data

    def get_vacancies_with_keyword(self, keywords: list):
        """  Метод получает список всех вакансий,
            в названии которых содержатся переданные
            в метод слова, например python.
            :type keywords: list[]
        """
        try:

            connection = psycopg2.connect(database=self.database_name, **self.params)
            with connection.cursor() as cursor:
                sql_string = "SELECT * FROM vacancies WHERE 1 = 0 "
                for el in keywords:
                    sql_string += f"OR lower(vacancy_title) LIKE '%{str(el)}%' "

                cursor.execute(sql_string)
                data = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        connection.close()
        return data


    def get_all_companies_in_request(self):
        """ Метод получает список всех компаний, полученных при запросе
        """
        try:
            connection = psycopg2.connect(database=self.database_name, **self.params)
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM companies;')
                data = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        connection.close()
        return data
