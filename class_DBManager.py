import psycopg2

from config.config import config


class DBManager(object):
    def __init__(self):
        self.db_name = 'hh_api_vacancies_db'
        self.__params = config()
        self.connect = psycopg2.connect(dbname=self.db_name, **self.__params)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.db_name})'

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            with self.connect.cursor() as cur:
                cur.execute("""SELECT DISTINCT employer_name, COUNT(*)
                               FROM employers
                               JOIN vacancies USING(vacancy_id)
                               GROUP BY employer_name""")
                total_vacancies = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return total_vacancies

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """

        try:
            with self.connect.cursor() as cur:
                cur.execute("""SELECT employers.employer_name, name_vacancy, salary, url
                                FROM vacancies
                                JOIN employers USING(vacancy_id)""")
                vacancies_list = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return vacancies_list

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        try:
            with self.connect.cursor() as cur:
                cur.execute("""SELECT AVG(salary)
                                FROM vacancies
                                        """)
                avg_salary = cur.fetchone()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        try:
            with self.connect.cursor() as cur:
                cur.execute("""SELECT name_vacancy
                                FROM vacancies
                                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                                """)
                vacancies = cur.fetchall()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return vacancies

    def get_vacancies_with_keyword(self, *args):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        vacancies = args
        vacancies_list = []
        try:
            with self.connect.cursor() as cur:
                for vacancy in vacancies:
                    word = '_' + vacancy[1:] + '%'
                    cur.execute("""SELECT name_vacancy
                                    FROM vacancies
                                    WHERE name_vacancy LIKE %s
                                    """,
                                (word,)
                                )
                    vacancies_list.extend(cur.fetchall())

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return vacancies_list

    def close_connect(self):
        self.connect.close()
