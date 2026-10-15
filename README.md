# Habr Career Vacancy Scraper / Парсер вакансий Хабр Карьера

[English](#english-version) | [Русский](#русская-версия)

---

## English Version

An interactive command-line (CLI) web scraper designed to automate job market monitoring on the popular Eastern European tech portal, Habr Career. The script dynamically filters vacancies by title and experience level (Intern to Lead), extracts vacancy details, and exports cleanly into Excel.

### --> Key Features
- **Custom User-Agent Header:** Integrates customized `User-Agent` HTTP headers to mimic organic browser sessions safely.
- **Fail-Safe & Robust Architecture:** Built-in fault tolerance handling (`if/else` fallbacks) preventing runtime exceptions when optional fields like salaries, skills, or locations are missing.
- **Dynamic URL Compiling:** Features an interactive menu to search for custom positions and filter precisely by 6 distinct experience levels.
- **Automated Pagination:** Seamlessly scans through multi-page results until completion.
- **Data Export:** Compiles dataframes using `Pandas` and saves them securely inside an isolated `/data` directory as a `.xlsx` file.

### --> Tech Stack
- **Python 3**
- **Requests** (Network communication & HTTP processing)
- **BeautifulSoup4 (lxml)** (DOM tree navigation & parsing)
- **Pandas** (Data engineering & Excel export)

### --> Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/xemalb0/habr-career-parser.git
   cd habr-career-parser
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## Русская Версия

Интерактивная консольная (CLI) утилита для автоматического мониторинга рынка труда и парсинга вакансий на ИТ-портале Хабр Карьера. Скрипт позволяет динамически искать вакансии по ключевым словам и уровню квалификации со встроенной автоматической генерацией параметров URL.

### --> Основные возможности
- **Интерактивный CLI-интерфейс:** Удобное консольное меню с нумерацией через `enumerate()`. Пользователь вводит название профессии и выбирает один из 6 уровней квалификации.
- **Безопасная сборка URL:** Реализована автоматическая замена пробелов в поисковом запросе на символы `+`. Это предотвращает поломку ссылок при вводе сложных названий (например, `Python Django`).
- **Защита от блокировок сайта:** Интеграция кастомных `User-Agent` заголовков в `requests` для успешной симуляции работы реального браузера.
- **Умная отказоустойчивость:** Архитектура защищена блоками `if/else`. Скрипт не падает со страшной ошибкой, если у вакансии отсутствует зарплатная вилка, навыки, дата публикации или геолокация.
- **Постраничная автоматизация:** Робот автономно находит кнопку «Next» на страницах Хабра, скачивает данные и останавливается сам, когда вакансии кончаются.
- **Изолированный экспорт данных:** Программа проверяет наличие папки `/data` на компьютере и создает её автоматически при отсутствии, защищая от ошибок `FileNotFoundError`. Итоговый Excel-файл именуется динамически под запрос пользователя.

### --> Стек технологий
- **Python 3**
- **Requests** (сетевые HTTP-запросы и получение кода страниц) [2]
- **BeautifulSoup4 (lxml)** (парсинг элементов верстки сайта) [2]
- **Pandas** (структурирование данных в DataFrame и экспорт в Excel) [2]

### --> Инструкция по запуску

1. Скачайте проект к себе на компьютер:
   ```bash
   git clone https://github.com/xemalb0/habr-career-parser.git
   ```
2. Установите необходимые библиотеки (зависимости):
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите парсер через консоль:
   ```bash
   python main.py
   ```
После завершения работы в созданной папке `data/` появится готовый отчет (например: `vacancy-habr-Python.xlsx`).