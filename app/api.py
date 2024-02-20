from datetime import datetime
from flask import Flask, jsonify, request, g
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            full_name varchar,
            created_at timestamp
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def start():
    return 'Desafio Ascan - Backend'

@app.route('/write', methods=['POST'])
def write_data():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO user (full_name, created_at) VALUES (?, ?)', (data['full_name'], current_time))
    db.commit()
    return jsonify({'message': 'Data written successfully'})

@app.route('/read', methods=['GET'])
def read_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user')
    rows = cursor.fetchall()
    user = [{'id': row[0], 'full_name': row[1], 'created_at': row[2]} for row in rows]
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
