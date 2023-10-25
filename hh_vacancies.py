import requests


class HeadHunterAPI():
    """Подключается к API HeadHunter и получает список вакансий по заданным критериям"""

    def __init__(self):
        self.base_url = 'https://api.hh.ru'

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.base_url})'

    def get_vacancies(self, data_company: dict):
        """
        Возвращает список вакансий по заданным работодателям
        """

        url = f'{self.base_url}/vacancies'
        all_vacancies = []

        params = {
            'page': 0,
            'per_page': 100,
            'employer_id': data_company.values()
        }
        while params['page'] != 10:
            response = requests.get(url, params=params)
            vacancies = response.json()['items']
            all_vacancies.extend(vacancies)
            params['page'] += 1
        return all_vacancies

