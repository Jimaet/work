import sqlite3
import pandas as pd

class ExcelToSQLite:
    def __init__(self, db_name="data.db"):
        # Создание базы данных SQLite (если она не существует)
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table_from_df(self, df, table_name):
        """
        Создание таблицы в SQLite из DataFrame.
        """
        # Определим столбцы и типы данных для SQL
        columns = ", ".join([f"{col} TEXT" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data_from_df(self, df, table_name):
        """
        Вставка данных из DataFrame в таблицу SQLite.
        """
        for row in df.itertuples(index=False, name=None):
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in row])})"
            self.cursor.execute(insert_query, row)
        self.conn.commit()

    def load_excel_to_sqlite(self, excel_file, sheet_name, table_name):
        """
        Загрузка данных из Excel в SQLite.
        """
        # Чтение данных из Excel в pandas DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Создание таблицы и вставка данных
        self.create_table_from_df(df, table_name)
        self.insert_data_from_df(df, table_name)
        print(f"Данные успешно импортированы в таблицу {table_name}")

    def fetch_data(self, table_name):
        """
        Получение всех данных из таблицы.
        """
        query = f"SELECT * FROM {table_name};"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()

# Пример использования
if __name__ == "__main__":
    # Путь к Excel файлу
    excel_file = 'your_file.xlsx'
    sheet_name = 'Sheet1'  # Имя листа
    table_name = 'my_table'

    # Создание объекта ExcelToSQLite
    excel_to_sqlite = ExcelToSQLite(db_name="my_database.db")

    # Загрузка данных из Excel в SQLite
    excel_to_sqlite.load_excel_to_sqlite(excel_file, sheet_name, table_name)

    # Получение данных из SQLite
    data = excel_to_sqlite.fetch_data(table_name)
    for row in data:
        print(row)

    # Закрытие соединения
    excel_to_sqlite.close()
