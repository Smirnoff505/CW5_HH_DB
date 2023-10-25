import psycopg2

from config.config import config
from config.const import COMPANY_DICT
from hh_vacancies import HeadHunterAPI
from utils import execute_sql_script, save_data_to_database


def main():
    script_file = 'fill_db.sql'
    db_name = 'hh_api_vacancies_db'

    params = config()

    vacancies = HeadHunterAPI().get_vacancies(COMPANY_DICT)
    connect = psycopg2.connect(dbname=db_name, **params)

    try:
        with connect.cursor() as cur:
            execute_sql_script(cur, script_file)
            print(f"В БД {db_name} успешно созданы таблицы")

            save_data_to_database(cur, vacancies)
            print(f'{db_name} успешно заполнена')

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    connect.commit()
    connect.close()


if __name__ == '__main__':
    main()
