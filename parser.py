import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
user_index = int(input('> Input:'))
print()
value = QUALIFICATION[list(QUALIFICATION.keys())[user_index - 1]]

search_link += '=' + user_search_encoded + '&' + value + 'type=all'

BASIC_LINK = 'https://career.habr.com' # direct link on site

vacancy_list = []
count_pages = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

response = requests.get(search_link, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

while True:
    vacancy_card_inner = soup.find_all('div', class_='vacancy-card__inner')
    for vacancy_card in vacancy_card_inner:
        data_time_class = vacancy_card.find('div', class_='vacancy-card__date')
        if data_time_class:
            data_time_link = data_time_class.find('time')
            data_time = data_time_link.text
        else:
            data_time = 'No publication date available / Дата не опубликована'

        vacancy_link = vacancy_card.find('a')
        vacancy_direct_link = BASIC_LINK + vacancy_link['href']
        
        vacancy_company_class = vacancy_card.find('div', class_='vacancy-card__company')
        if vacancy_company_class:
            vacancy_company_link = vacancy_company_class.find('a')
            vacancy_company_info_link = BASIC_LINK + vacancy_company_link['href']
            vacancy_company = vacancy_company_link.text
        else:
            vacancy_company = 'Company name not specified / Название компании не указано'
        
        vacancy_title_class = vacancy_card.find('div', class_='vacancy-card__title')
        if vacancy_title_class:   
            vacancy_title_link = vacancy_title_class.find('a')
            vacancy_title = vacancy_title_link.text # название вакансии
        else:
            vacancy_title = 'Untitled Position / Название вакансии не указано'

        vacancy_salary_class = vacancy_card.find('div', class_='basic-salary')
        if vacancy_salary_class:
            vacancy_salary = vacancy_salary_class.text # указание зарплаты, если она указана
        else:
            vacancy_salary = 'Salary not specified / Зарплата не указана'

        vacancy_card_meta = vacancy_card.find('div', class_='vacancy-meta')
        if vacancy_card_meta:
            vacancy_meta = vacancy_card_meta.find_all('div', class_='chip-with-icon__text')
            vacancy_data_meta = [meta.text.strip() for meta in vacancy_meta]
            meta = ', '.join(vacancy_data_meta)
        else:
            meta = 'Location and position not specified / Расположение и позиция не указана'

        vacancy_card_skill = vacancy_card.find('div', class_='vacancy-card__skills')
        if vacancy_card_skill:
            vacancy_skill_link = vacancy_card_skill.find_all('div', class_='basic-chip__text')
            vacancy_skill_list = [skill.text for skill in vacancy_skill_link] if vacancy_skill_link else 'Нет данных'
            vacancy_skill = ', '.join(vacancy_skill_list)
        else:
            vacancy_skill = 'Skills not specified / Навыки не указаны'

        vacancy_list.append({'Publication Date': data_time,
                             'Company': vacancy_company,
                             'Job Title': vacancy_title,
                             'Salary': vacancy_salary,
                             'Level and Location': meta,
                             'Skills': vacancy_skill,
                             'Vacancy Link': vacancy_direct_link,
                             'Company Link': vacancy_company_info_link
                            }) 
    count_pages += 1
    print(f'Page {count_pages} is Done.')

    nav_page_box = soup.find('a', class_='page next')
    if nav_page_box:
        next_link = 'https://career.habr.com' + nav_page_box['href']
        response = requests.get(next_link, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
    else:
        print('Data collection completed')
        break

df = pd.DataFrame(vacancy_list)

if not os.path.exists('data'):
    os.makedirs('data')
df.to_excel(f'data/vacancy-habr-{user_search}.xlsx', sheet_name='Vacancy List', index=False)
print('Data successfully exported to Excel.')

