from datetime import datetime


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения таблицами БД данными."""
    with open(script_file, 'r') as file:
        sql_script = file.read()
    cur.execute(sql_script)


def save_data_to_database(cur, vacancies):
    """Сохранение вакансий и работодателей в базе данных"""
    for vacancy in vacancies:
        date_obj = datetime.strptime(vacancy['published_at'][:10], '%Y-%m-%d')
        format_date = datetime.strftime(date_obj, '%d-%m-%Y')
        data_description = vacancy['snippet']
        salary_data = vacancy['salary']
        if salary_data is None:
            salary = None
        else:
            if salary_data['currency'] == 'USD':
                salary = salary_data['from'] * 93
            else:
                salary = salary_data['from']

        cur.execute(
            """INSERT INTO vacancies (name_vacancy, salary, city, url, requirement, responsibility, create_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING vacancy_id""",
            (vacancy['name'], salary, vacancy['area']['name'], vacancy['alternate_url'],
             data_description['requirement'], data_description['responsibility'], format_date)
                    )
        vacancy_id = cur.fetchone()[0]
        employers = vacancy['employer']
        cur.execute(
            """INSERT INTO employers (employer_id, employer_name, vacancy_id) VALUES (%s, %s, %s)""",
            (employers['id'], employers['name'], vacancy_id)
        )
