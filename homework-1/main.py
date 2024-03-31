# """Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import pathlib
import csv

# Коннект к БД
conn = psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password="1"
)

# Курсор к БД
cur = conn.cursor()

# Список таблиц БД для заполнения
tables_db = ['employees', 'customers', 'orders']
# Список имен файлов *.cvs c данными
files_cvs = ['customers_data.csv', 'employees_data.csv', 'orders_data.csv']
# Заполнение таблиц в БД данными
for table in tables_db:
    for file in files_cvs:
        if table in file:
            path_file = pathlib.Path.cwd() / 'north_data' / file
            with open(path_file, "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    mask = ('%s,' * len(row))[:-1]
                    cur.execute(f"INSERT INTO {table} VALUES ({mask})", row)
                conn.commit()
cur.close()
conn.close()
