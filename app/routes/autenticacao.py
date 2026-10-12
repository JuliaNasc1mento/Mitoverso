from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models.usuario import Usuario
from app.form.cadastro_form import CadastroForm
from app.form.login_form import LoginForm

# Criação do Blueprint "login"
autenticacao_bp = Blueprint("autenticacao", __name__)

@login_manager.user_loader
def carregar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))

@autenticacao_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        usuario = db.session.scalar(db.select(Usuario).filter_by(email=email))

        if usuario:
            flash("E-mail já cadastrado.", "warning")
        else:
            novo_usuario = Usuario(nome=form.nome.data.strip(), email=email, senha=generate_password_hash(form.senha.data))

            db.session.add(novo_usuario)
            db.session.commit()

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("autenticacao.login"))
        
    return render_template("usuario/cadastro.html", form=form)

@autenticacao_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        usuario = db.session.scalar(db.select(Usuario).filter_by(email=email))

        if usuario and check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            return redirect(url_for("principal"))

        flash("E-mail ou senha incorretos.", "danger")

    return render_template("usuario/login.html", form=form)

@autenticacao_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("principal"))
