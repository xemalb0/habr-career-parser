import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
import json


BASE_URL = 'https://career.habr.com/vacancies?'
HABR_LINK = 'https://career.habr.com'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def scraping_page(html):
    vacancy_list = []
    soup = BeautifulSoup(html, 'lxml')
    vacancy_card_inner = soup.find_all('div', class_='vacancy-card__inner')
    for vacancy_card in vacancy_card_inner:
        data_time_class = vacancy_card.find('div', class_='vacancy-card__date')
        if data_time_class:
            data_time_link = data_time_class.find('time')
            data_time = data_time_link.text
        else:
            data_time = 'No publication date available / Дата не опубликована'

        vacancy_link = vacancy_card.find('a')
        vacancy_direct_link = HABR_LINK + vacancy_link['href']
        
        vacancy_company_class = vacancy_card.find('div', class_='vacancy-card__company')
        if vacancy_company_class:
            vacancy_company_link = vacancy_company_class.find('a')
            vacancy_company_info_link = HABR_LINK + vacancy_company_link['href']
            vacancy_company = vacancy_company_link.text
        else:
            vacancy_company = 'Company name not specified / Название компании не указано'
            vacancy_company_info_link = 'Company link not specified / Сайт компании не указан'
        
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
            vacancy_skill_list = [
            skill.text.strip() for skill in vacancy_skill_link
            ] if vacancy_skill_link else []
            vacancy_skill = ', '.join(vacancy_skill_list) or 'Нет данных'
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
    return vacancy_list

async def catch_page(session: aiohttp.ClientSession, url: str) -> str:
    start_time = time.strftime('%X')
    print(f'{start_time} - [Старт] Отправка запроса к странице.')
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            end_time = time.strftime('%X')
            if response.status == 200:
                print(f'{end_time} - [Стоп] Ответ получен - [{response.status}]. Страница загружена.')
                return await response.text()
            else:
                print(f'{end_time} - [Стоп] Ответ получен - [{response.status}]. Страница не загружена.')
                return ''
    except Exception as e:
        end_time = time.strftime('%X')
        print(f'{end_time} - [Ошибка] Ошибка обращения к серверу: {e}')
        return ''

async def scouting(session: aiohttp.ClientSession, url: str):
    html = await catch_page(session, url)
    if not html:
        return [], []
    soup = BeautifulSoup(html, 'lxml')
    script = soup.find('script', attrs={'data-ssr-state': 'true'})
    if script is None:
        raise RuntimeError('[Ошибка] Скрипт не получен.')
    else:
        data = json.loads(script.string)
        total_pages = [i for i in range(2, int(data['vacancies']['meta']['totalPages']) + 1)]
        first_page_vacancied = scraping_page(html)
        return total_pages, first_page_vacancied


async def parse_single_page(session: aiohttp.ClientSession, url: str, page_num: int):
    start_time = time.strftime('%X')
    print(f'{start_time} - [Старт] Скачиваю страницу...')
    html = await catch_page(session, url)
    if not html:
        return []
    vacansies = scraping_page(html)
    end_time = time.strftime('%X')
    print(f'{end_time} - [Стоп] Страница {page_num} обработана.')
    return vacansies

async def main_scrapper(part_of_link, first_page_link):
    start_parsing_time = time.time()
    total_pages = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        total_pages, first_page_vacancied = await scouting(session, first_page_link)
        for page in total_pages:
            page_url = BASE_URL + f'page={page}&' + part_of_link
            task = parse_single_page(session, page_url, page)
            tasks.append(task)
        result = await asyncio.gather(*tasks)
        final_vacancies = []
        final_vacancies.extend(first_page_vacancied)
        for page_data in result:
            final_vacancies.extend(page_data)
        end_parsing_time = time.time()
        print(f'Парсинг завершён за время: {end_parsing_time - start_parsing_time:.2f}')
        print(f'Собрано вакансий: {len(final_vacancies)}')
        return final_vacancies

if __name__ == '__main__':
    asyncio.run(main_scrapper())