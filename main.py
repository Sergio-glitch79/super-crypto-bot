from flask import Flask

app = Flask(__name__)

# Главная страница — просто проверка, что всё работает
@app.route('/')
def home():
    return 'Супербот работает!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
