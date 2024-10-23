from jogoteca import app
from helpers import FormularioUsuario
from flask import request, render_template, session, flash, redirect, url_for
from models import Usuarios
from flask_bcrypt import check_password_hash

# pega os args da requisição /login e armazena na variável proxima, que será armazenada em value do input da página login.html
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

# recebe o valor de proxima do input de login.html e faz o redirect concatenando, que nesse caso o resultado será "/novo"
@app.route('/autenticar', methods=['POST',])
def autenticar():
    # pega os valores submetidos no formulario e armazena na variavel
    form = FormularioUsuario(request.form)
    # No BD, procura o primeiro usuario que tiver o nickname igual ao nickname fornecido no formulário
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    # checa se a senha do banco eh igual a senha fornecida no form
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
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