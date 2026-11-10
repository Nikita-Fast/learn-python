
import io
import numpy as np


# Адаптер: NumPy-массив -> BLOB
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return out.read()


# Конвертер: BLOB -> NumPy-массив
def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


if __name__ == '__main__':
    import sqlite3

    # Регистрируем адаптеры в sqlite3
    sqlite3.register_adapter(np.ndarray, adapt_array)
    sqlite3.register_converter("NDARRAY", convert_array)

    conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE test_table (id INTEGER, data NDARRAY)")

    # Создаем тестовый массив
    arr = np.random.rand(50001)

    # Сохранение (массив передается напрямую)
    cursor.execute("INSERT INTO test_table (id, data) VALUES (?, ?)", (1, arr))
    conn.commit()

    # Извлекаем массив (вернется np.ndarray)
    cursor.execute("SELECT data FROM test_table WHERE id = 1")
    retrieved_arr = cursor.fetchone()[0]

    if np.array_equal(arr, retrieved_arr):
        print("Успех! Массивы идентичны")
        print(f"{arr.shape=}")
        print(f"{retrieved_arr.shape=}")
        print(f"{arr[:5]=}")
        print(f"{retrieved_arr[:5]=}")
    else:
        print("Ошибка! Массивы не равны")
