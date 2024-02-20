from flask import Flask

app = Flask(__name__)

@app.route('/')
def start():
    return 'Desafio Ascan - Backend'

@app.route('/teste')
def info():
    return 'Testando!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
