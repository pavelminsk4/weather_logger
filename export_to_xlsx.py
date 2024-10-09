from dotenv import load_dotenv
import os
import pandas as pd
import sqlite3


def exp_to_xlsx():
    load_dotenv()
    count = os.getenv('LINES_COUNT')

    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect('db.db')  # Укажите имя вашей базы данных

    # Запрашиваем последние 10 записей
    # Укажите свою таблицу и поле для сортировки
    query = f"SELECT * FROM records ORDER BY record_id DESC LIMIT {count}"
    df = pd.read_sql_query(query, conn)

    # Закрываем соединение с базой данных
    conn.close()

    # Сохраняем DataFrame в файл XLSX
    df.to_excel(f'last_{count}_records.xlsx', index=False)

    print(f"Last {count} records saved to last_{count}_records.xlsx")
