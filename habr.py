import requests
from bs4 import BeautifulSoup
import sqlite3
import telebot

API_KEY = '7215397063:AAFBjiVWT7Uzje5T6QBHO7QUbWa9Z0OkrlU'
bot = telebot.TeleBot(API_KEY)

URL = 'https://career.habr.com/vacancies?type=all'
MAX_PAGE = 150
headers = {
    'Host': 'career.habr.com',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

user_state = {}

# Функции для парсинга данных с Habr
def extract_job(html):
    title = html.find('div', {'class': 'vacancy-card__title'}).find('a').text
    link = 'https://career.habr.com' + html.find('a')['href']
    company = html.find('div', {'class': 'vacancy-card__company-title'}).find('a').text
    info = html.find('div', {'class': 'vacancy-card__meta'}).text
    return {'title': title, 'company': company, 'info': info, 'link': link}

def extract_habr_jobs(max_page, city_filter=None, company_filter=None, profession_filter=None):
    jobs = []
    for page in range(1, max_page + 1):
        print('Парсинг career.habr.com, страница:', page)
        result = requests.get(f'{URL}&page={page}', headers=headers)
        soup = BeautifulSoup(result.text, 'lxml')

        check = soup.find('div', {'class': 'no-content__title'})
        if check and check.text.strip() == 'Поиск не дал результатов':
            break

        results = soup.find_all('div', {'class': 'vacancy-card__info'})
        for result in results:
            job = extract_job(result)
            if city_filter and city_filter.lower() not in job['info'].lower():
                continue
            if company_filter and company_filter.lower() not in job['company'].lower():
                continue
            if profession_filter and profession_filter.lower() not in job['title'].lower():
                continue
            jobs.append(job)
    return jobs

def get_jobs(city=None, company=None, profession=None):
    return extract_habr_jobs(MAX_PAGE, city_filter=city, company_filter=company, profession_filter=profession)

# Функции для работы с базой данных
def create_database():
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            info TEXT,
            link TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

def insert_jobs(cursor, jobs):
    cursor.execute('DELETE FROM jobs')
    for job in jobs:
        cursor.execute('''
            INSERT INTO jobs (title, company, info, link) VALUES (?, ?, ?, ?)
        ''', (job['title'], job['company'], job['info'], job['link']))

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id,
                     'Здравствуйте! Этот бот позволит вам найти работу своей мечты! '
                     'Он найдет все вакансии по вашему запросу с сайта Habr. '
                     'Когда будете готовы, напишите цифру "1", и бот вышлет вам инструкцию пользования.')

@bot.message_handler(func=lambda message: message.text == "1")
def send_instruction(message):
    instruction = (
        "Инструкция пользования:\n\n"
        "1. Введите название города для фильтрации вакансий (или оставьте пустым, если не нужно).\n"
        "2. Введите название компании для фильтрации вакансий (или оставьте пустым, если не нужно).\n"
        "3. Введите название профессии для фильтрации вакансий (или оставьте пустым, если не нужно).\n\n"
        "Введите данные через запятые (например: Москва, Яндекс, Python разработчик) или оставьте пустыми, если не хотите фильтрации.\n"
    )
    bot.send_message(message.chat.id, instruction)

@bot.message_handler(func=lambda message: message.text == "дальше")
def show_next_jobs(message):
    user_id = message.chat.id
    if user_id in user_state and user_state[user_id]['jobs']:
        start = user_state[user_id]['index']
        end = start + 5
        jobs = user_state[user_id]['jobs'][start:end]
        user_state[user_id]['index'] = end

        if not jobs:
            bot.send_message(user_id, "Больше вакансий нет.")
        else:
            for job in jobs:
                bot.send_message(
                    user_id,
                    f"Заголовок: {job['title']}\nКомпания: {job['company']}\nИнформация: {job['info']}\nСсылка: {job['link']}"
                )
            
            if end < len(user_state[user_id]['jobs']):
                bot.send_message(user_id, "Напишите 'дальше', чтобы увидеть следующие вакансии.")
            else:
                bot.send_message(user_id, "Это все вакансии по вашему запросу.")
    else:
        bot.send_message(user_id, "Пожалуйста, выполните новый запрос для просмотра вакансий.")

@bot.message_handler(func=lambda message: True)
def get_vacancies(message):
    user_input = message.text.split(',')
    city = user_input[0].strip() if len(user_input) > 0 else None
    company = user_input[1].strip() if len(user_input) > 1 else None
    profession = user_input[2].strip() if len(user_input) > 2 else None

    bot.send_message(message.chat.id, "Загрузка вакансий, пожалуйста, подождите...")

    habr_jobs = get_jobs(city=city, company=company, profession=profession)

    if not habr_jobs:
        bot.send_message(message.chat.id, "Не найдено вакансий по заданным параметрам.")
    else:
        conn, cursor = create_database()
        insert_jobs(cursor, habr_jobs)
        conn.commit()
        conn.close()

        user_state[message.chat.id] = {'jobs': habr_jobs, 'index': 0}
        show_next_jobs(message)

bot.polling()