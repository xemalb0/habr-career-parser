import os
from scrapers import *
from export import export_to_excel

vacancy_list = []
search_link = 'https://career.habr.com/vacancies?q'

QUALIFICATION = {'Intern/Стажёр': 'qid=1&',
                 'Junior/Младший': 'qid=3&',
                 'Middle/Средний': 'qid=4&',
                 'Senior/Старший': 'qid=5&',
                 'Lead/Ведущий': 'qid=6&',
                 'Any/Любая': ''}

print('Welcome to the Habr Vacancy Scraper CLI!\n')
print('Enter job title to search: ')

user_search = input('> Input:').strip()
user_search_encoded = user_search.replace(' ', '%20')

print('\nAvailable Experience Levels:')

for i, k in enumerate(QUALIFICATION):
    print(f'{i + 1}. {k}')

print('\nEnter level number: ')

while True:
    try:
        user_index = int(input('> Input:'))
        value = QUALIFICATION[list(QUALIFICATION.keys())[user_index - 1]]
    except IndexError:
        print('\nIncorrect index entered')
        continue
    except ValueError:
        print('\nIncorrect index entered')
        continue
    else:
        break

search_link += '=' + user_search_encoded + '&' + value + 'type=all'

parsing_habr(search_link, vacancy_list)
export_to_excel(vacancy_list, user_search)

