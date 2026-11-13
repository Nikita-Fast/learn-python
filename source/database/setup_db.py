import sqlite3

import numpy as np

from source.database.array_adapter import adapt_array, convert_array


if __name__ == '__main__':
    print(f"Версия движка sqlite: {sqlite3.sqlite_version}\n")

    # Регистрируем адаптеры в sqlite3
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("NDARRAY", convert_array)

    # temporary RAM-only database
    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Создание схемы базы данных
    with open("schema.sql", "r", encoding="utf-8") as file:
        cursor.executescript(file.read())

    # Заполнение базы данных данными
    with open("seed.sql", "r", encoding="utf-8") as file:
        cursor.executescript(file.read())

    conn.commit()


    # Просмотр содержимого таблиц
    cursor.execute("SELECT * FROM parameters")
    rows = cursor.fetchall()
    print("Строки таблицы 'parameters':")
    for x in rows:
        print(x)
    print()

    cursor.execute("""
        SELECT parameters.name, parameter_ppm_channels.ppsm
        FROM parameter_ppm_channels JOIN parameters
        ON parameter_ppm_channels.parameter_id = parameters.id
    """)
    rows = cursor.fetchall()
    print("Строки таблицы 'parameter_ppm_channels':")
    for x in rows:
        print(x)
    print()

    cursor.close()
    conn.close()
