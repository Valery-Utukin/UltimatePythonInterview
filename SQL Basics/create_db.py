import sqlite3
import random
from faker import Faker
from contextlib import contextmanager


@contextmanager
def cursor_sqlite():
    conn = sqlite3.connect("people.db")
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()


def create_table(table_name: str, attributes: dict, cur) -> None:
    columns = [f"{key} {value}" for key, value in attributes.items()]
    table_query = ", ".join(columns)

    # Создание таблицы
    try:
        cur.execute(f"""DROP TABLE IF EXISTS {table_name}""")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_query})""")
    except Exception as e:
        print(f"Cannot create table: {e}")


def print_all_rows(table_name: str):
    with cursor_sqlite() as cur:
        rows = cur.execute(f"SELECT * FROM {table_name}")
        for row in rows:
            print(row)


def main():
    """
    Create people.db with two tables (users, developers) and fill them up with dummy data using Faker lib.

    :return: None
    """

    fake = Faker()

    users_columns_dict = {
        'id': "INTEGER PRIMARY KEY AUTOINCREMENT",
        'first_name': "TEXT NOT NULL",
        'last_name': "TEXT NOT NULL",
        'age': "INTEGER",
        'phone': "TEXT UNIQUE",
        'email': "TEXT UNIQUE",
        'city': "TEXT",
        'reg_date': "TEXT",
    }

    developers_columns_dict = {
        'id': "INTEGER PRIMARY KEY AUTOINCREMENT",
        'first_name': "TEXT NOT NULL",
        'last_name': "TEXT NOT NULL",
        'age': "INTEGER",
        'city': "TEXT",
        'prog_ln': "TEXT NOT NULL",
        'salary': "INTEGER NOT NULL"
    }

    # Создание БД people.db и заполнение таблиц
    with cursor_sqlite() as cur:
        create_table(table_name="users", attributes=users_columns_dict, cur=cur)
        create_table(table_name="developers", attributes=developers_columns_dict, cur=cur)

        # Наполняем таблицу users фейковыми пользователями
        for _ in range(100):
            fn = fake.first_name()
            ln = fake.last_name()
            a = random.randint(16, 80)
            p = fake.phone_number()
            e = fake.email()
            c = fake.city()
            rd = fake.iso8601()

            cur.execute("INSERT INTO users (first_name, last_name, age, phone, email, city, reg_date)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?)", (fn, ln, a, p, e, c, rd))

        # Наполняем таблицу developers фейковыми разработчиками
        prog_languages = ["C/C++", "Java", "JavaScript", "Python", "C#", "Pascal???", "Rust", "GO", "Ruby",
                          "HTML/CSS", "PHP", "Fortran", "1C", "SQL", "Kotlin", "Swift"]
        for _ in range(100):
            fn = fake.first_name()
            ln = fake.last_name()
            a = random.randint(16, 80)
            c = fake.city()
            pl = random.choice(prog_languages)
            s = random.randint(500, 10000)

            cur.execute("INSERT INTO developers (first_name, last_name, age, city, prog_ln, salary)"
                        "VALUES (?, ?, ?, ?, ?, ?)", (fn, ln, a, c, pl, s))


if __name__ == '__main__':
    main()

    print_all_rows(table_name="users")
    print_all_rows(table_name="developers")
