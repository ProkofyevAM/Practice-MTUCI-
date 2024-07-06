import sqlite3

def view_database():
    # Подключение к базе данных
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных
    cursor.execute('SELECT * FROM jobs')

    # Получение всех строк результата запроса
    rows = cursor.fetchall()

    # Вывод строк
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Заголовок: {row[1]}")
        print(f"Компания: {row[2]}")
        print(f"Информация: {row[3]}")
        print(f"Ссылка: {row[4]}")
        print("\n" + "-"*50 + "\n")

    # Закрытие соединения с базой данных
    conn.close()

if __name__ == '__main__':
    view_database()