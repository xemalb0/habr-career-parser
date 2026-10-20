# Habr Career Parser

A Python parser for collecting vacancies from Habr Career (https://career.habr.com/).

---

## Features

- **Asynchronous HTTP requests with aiohttp
- **Vacancy data extraction with BeautifulSoup4
- **Export to Excel using pandas

---

## Tech Stack
- **Python
- **aiohttp
- **BeautifulSoup4
- **pandas
- **openpyxl

---

## Installation

```bash
git clone https://github.com/xemalb0/habr-career-parser.git
cd habr-career-parser
python -m venv .venv
```
## Activate the virtual environment:
### Windows
```bash
.venv\Scripts\activate
```
###Linux / macOS
```bash
source .venv/bin/activate
```
###Install dependencies:
```bash
pip install -r requirements.txt
```
##Usage
```bash
python main.py
```
The collected data is exported to an Excel file.
##Disclaimer
This project is intended for educational purposes.
Please respect the website’s terms of use and access limits.