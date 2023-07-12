Бот в телеграмме https://t.me/adsf_asdf_python_project_bot показывает текущий курс и изменения за последние 24 часа выбранных криптовалют

Все зависимости лежат в файле requirements.txt

Проект состоит из двух частей:
1) (parsing.py) Парсинг всех неймингов криптовалют с сайта CoinMarketCup в файлик crypto_list.csv
2) Сам бот, который использует в том числе данные, полученные в предыдущем пункте

Запуск проекта:
1) Клонируйте репозиторий: git clone <...>
2) Чтобы утановить все зависимости: pip3 install -r requirements.txt
3) Получаем данные с сайта (Выполняется один раз): python3 parsing.py
4) Запуск бота: python3 bot.py

Для начала работы бота введите /start

![Image alt](https://github.com/fomaivan/python_telegram_bot/blob/main/images/start.png) 

![Image alt](https://github.com/fomaivan/python_telegram_bot/blob/main/images/help.png)

![Image alt](https://github.com/fomaivan/python_telegram_bot/blob/main/images/all.png)

![Image alt](https://github.com/fomaivan/python_telegram_bot/blob/main/images/add.png)

![Image alt](https://github.com/fomaivan/python_telegram_bot/blob/main/images/del.png)
