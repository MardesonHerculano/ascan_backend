from datetime import datetime
from flask import Flask, jsonify, request, g
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

def create_user_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            full_name varchar,
            created_at timestamp
        )
    ''')

def create_subscription_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscription (
            id INTEGER PRIMARY KEY,
            user_id int,
            status_id int,
            created_at timestamp,
            updated_at timestamp
        )
    ''')

def create_event_history_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_history (
            id INTEGER PRIMARY KEY,
            subscription_id int,
            type varchar,
            created_at timestamp
        )
    ''')

def create_status_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY,
            status_name varchar
        )
    ''')

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    create_user_table(cursor)
    create_subscription_table(cursor)
    create_event_history_table(cursor)
    create_status_table(cursor)
    
    conn.commit()
    conn.close()

create_tables()

@app.route('/')
def start():
    return 'Desafio Ascan - Backend'

def user_exists(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Converter 'user_id' para uma tupla para evitar o erro
    cursor.execute('SELECT id FROM user WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


@app.route('/write', methods=['POST'])
def write_data():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO user (full_name, created_at) VALUES (?, ?)', (data['full_name'], current_time))
    db.commit()
    return jsonify({'message': 'Data written successfully'})

@app.route('/subscription', methods=['POST'])
def subscription():
    data = request.json
    user_id = data.get('user_id')
    
    if user_id is None:
        return jsonify({'error': 'Missing user_id parameter'}), 400
    
    if not user_exists(user_id):
        return jsonify({'error': 'User does not exist'}), 404
    
    db = get_db()
    cursor = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO subscription (user_id, status_id, created_at, updated_at) VALUES (?, ?, ?, ?)', (user_id, data['status_id'], current_time, current_time))

    db.commit()
    return jsonify({'message': 'Subscription successful'})

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
