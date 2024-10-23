from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem, deleta_arquivo
import time

@app.route('/')
def index():
    #ordena os jogos por ID vindos do BD
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo="Jogos", jogos=lista)

# se não estiver logado, redireciona para login, passando a varivavel 'proxima' como novo (Quando o login terminar queremos retornar a pagina novo)
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    # verifica se algum jogo com esse nome já existe
    jogo = Jogos.query.filter_by(nome=nome).first()
    
    # caso exista, retorna ao index
    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))
    
    # cria uma instância na tabela Jogos
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    # adiciona o jogo no BD e commita
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']

    # evita o funcionamento padrão do cache, definindo um identificador único toda vez que a capa é atualizada, forçando a aplicação a fazer um request novamente.
    timestamp = time.time()

    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    # busca o jogo pelo ID
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)
    
@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']

    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    #deleta o jogo com ID especifico do banco de dados
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))

# pega os args da requisição /login e armazena na variável proxima, que será armazenada em value do input da página login.html
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

# recebe o valor de proxima do input de login.html e faz o redirect concatenando, que nesse caso o resultado será "/novo"
@app.route('/autenticar', methods=['POST',])
def autenticar():
    # No BD, procura o primeiro usuario que tiver o nickname igual ao nickname fornecido no formulário
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))  

@app.route('/logout') 
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index')) 

@app.route(f'/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

