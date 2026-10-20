from scraper import *
from export import *

QUALIFICATION = {'Intern': 'qid=1&',
                 'Junior': 'qid=3&',
                 'Middle': 'qid=4&',
                 'Senior': 'qid=5&',
                 'Lead': 'qid=6&',
                 'Any': ''}
BASE_URL = 'https://career.habr.com/vacancies?'
print('Добро пожаловать в парсер Хабр-карьеры!\n')
print('Введите название вакансии для поиска: ')

user_search = input('> Input:').strip()
user_search_encoded = user_search.replace(' ', '%20')

print('\nТипы квалификации:')

for i, k in enumerate(QUALIFICATION):
    print(f'{i + 1}. {k}')

print('\nВыберите номер: ')

while True:
        try:
            user_index = int(input('> Input:'))
            if 1 <= user_index <= len(QUALIFICATION):
                value = QUALIFICATION[list(QUALIFICATION.keys())[user_index - 1]]
                qualification = next((k for k, v in QUALIFICATION.items() if v == value), None)
                break
            else:
                print('Неверный введенный ин')
        except IndexError:
            print('\nIncorrect index entered')
            continue
        except ValueError:
            print('\nIncorrect index entered')
            continue
        else:
            break
part_of_link = 'q=' + user_search_encoded + '&' + value + 'type=all' # часть ссылки, для перемещения по страницам.
first_page_link = BASE_URL + part_of_link # ссылка для первого поиска по запросу.
if __name__ == '__main__':
    vacancy_list = []
    vacancy_list.extend(asyncio.run(main_scrapper(part_of_link, first_page_link)))
    export_to_excel(vacancy_list, user_search, qualification)
