import sqlite3
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


def main():
    with cursor_sqlite() as cur:
        res = cur.execute("SELECT salary FROM developers "
                          "WHERE prog_ln = 'Python'"
                          "ORDER BY salary DESC")
        for row in res:
            print(row)


if __name__ == '__main__':
    main()
