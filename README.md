# Practice-MTUCI-
1. habr.py является главным файлом содержащий в себе Парсинг всех вакансий с сайта "Habr.Карьера" с дальнейшим интегрированием их в Базу данных SQLite.
2. vacancies.db - файл с базой данных, чтобы его прочитать нужно использовать код из файла reader.py
3. В качестве веб-интерфейса в файле habr.py также реализован телеграм-бот по ссылке - https://t.me/HabrParcer_bot с его помощью пользователь может получить инструкцию о его работе, искать вакансии по желаемым фильтрам и выводить аналитику кол-ва вакансий. (ВНИМАНИЕ: Бот достаточно примитивный и не стоит злоупотреблять его функциями, он ломается)
4. Тестирование системы было проведено много раз - всё работает.

Инструкция пользования ботом:
        1. Введите название города для фильтрации вакансий (или оставьте пустым, если не нужно).
        2. Введите название компании для фильтрации вакансий (или оставьте пустым, если не нужно).
        3. Введите название профессии для фильтрации вакансий (или оставьте пустым, если не нужно).
        Введите данные через запятые (например: Москва, Яндекс, Python разработчик) или оставьте пустыми, если не хотите фильтрации.
   
   
