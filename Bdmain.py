from flask import Flask, request, jsonify
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создание базы данных и таблицы (если они не существуют)
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        column1 TEXT,
                        column2 TEXT,
                        column3 TEXT)''')  # Пример таблицы с 3 столбцами
    conn.commit()
    conn.close()

# Функция для загрузки данных из Excel в SQLite
def upload_excel_to_db(file_path):
    # Чтение данных из Excel в pandas DataFrame
    df = pd.read_excel(file_path)

    # Подключение к базе данных SQLite
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Запись данных в таблицу
    for _, row in df.iterrows():
        cursor.execute('INSERT INTO data (column1, column2, column3) VALUES (?, ?, ?)',
                       (row['column1'], row['column2'], row['column3']))  # Пример вставки данных
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload_file():
    # Проверка, что файл был передан
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден"}), 400

    file = request.files['file']

    # Проверка формата файла
    if file and file.filename.endswith('.xlsx'):
        # Сохранение файла на сервере
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

        # Загрузка данных из Excel в БД
        try:
            upload_excel_to_db(file_path)
            return jsonify({"message": f"Данные из {file.filename} успешно загружены в базу данных!"}), 200
        except Exception as e:
            return jsonify({"error": f"Произошла ошибка при загрузке данных: {str(e)}"}), 500
    else:
        return jsonify({"error": "Неверный формат файла. Пожалуйста, загрузите файл .xlsx."}), 400

if __name__ == '__main__':
    # Инициализация базы данных
    init_db()
    # Запуск Flask-сервера
    app.run(debug=True)
