import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(
        user="", # свой user
        password="", # свой password
        host="", # свой host
        port="" # свой port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE chain;")
    print("База данных 'chain' успешно создана!")

    cursor.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Ошибка при создании базы данных: {e}")