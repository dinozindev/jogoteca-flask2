import os

SECRET_KEY = 'alura'

# string de conexão com o banco de dados
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'jogoteca'
    )

# caminho absoluto do diretorio (jogoteca2) / uploads
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'