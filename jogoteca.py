#Flask==3.0.3
#mysql-connector-python==8.0.28
#Flask-SQLAlchemy==3.0.3
#Flask-WTF==1.0.0
#Flask-Bcrypt==1.0.1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# pega as configurações da aplicação a partir de outro arquivo
app.config.from_pyfile('config.py')

# cria instância de SQLAlchemy, inicializando a conexão com o banco de dados.
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)