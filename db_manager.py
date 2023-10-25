from pprint import pprint

from class_DBManager import DBManager

db_manager = DBManager()

pprint(db_manager.get_vacancies_with_keyword('python', 'java'))

pprint(db_manager.get_vacancies_with_higher_salary())

print(db_manager.get_avg_salary())

pprint(db_manager.get_all_vacancies())

pprint(db_manager.get_companies_and_vacancies_count())

db_manager.close_connect()
