from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos 
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
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
        form = FormularioJogo()
        return render_template('novo.html', titulo='Novo Jogo', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    #nome = request.form['nome']
    #categoria = request.form['categoria']
    #console = request.form['console']

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
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

    # pega a capa inserida no formulario
    arquivo = request.files['arquivo']
    # define o upload_path a partir da variavel global em config.py
    upload_path = app.config['UPLOAD_PATH']

    # evita o funcionamento padrão do cache, definindo um identificador único toda vez que a capa é atualizada, forçando a aplicação a fazer um request novamente.
    timestamp = time.time()

    # salva o arquivo no diretorio com o novo de arquivo sendo id + timestamp + .jpg
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    # busca o jogo pelo ID
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)
    
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        #jogo.nome = request.form['nome']
        #jogo.categoria = request.form['categoria']
        #jogo.console = request.form['console']

        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

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

 

@app.route(f'/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

