#Flask==3.0.3
#mysql-connector-python==8.0.28
#Flask-SQLAlchemy==3.0.3
#Flask-WTF latest
#Flask-Bcrypt==1.0.1
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
# pega as configurações da aplicação a partir de outro arquivo
app.config.from_pyfile('config.py')

# cria instância de SQLAlchemy, inicializando a conexão com o banco de dados.
db = SQLAlchemy(app)
# cria instância de CSRF
csrf = CSRFProtect(app)
# cria instancia de Bcrypt
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)