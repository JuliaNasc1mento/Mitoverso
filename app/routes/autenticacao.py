
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import db, login_manager
from app.models.usuario import Usuario
from app.form.cadastro_form import CadastroForm
from app.form.login_form import LoginForm
from app.services.usuario_service import (
    buscar_por_email,
    cadastrar_usuario,
    verificar_senha
)

autenticacao_bp = Blueprint("autenticacao", __name__)

@login_manager.user_loader
def carregar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))

@autenticacao_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = CadastroForm()

    if form.validate_on_submit():
        nome = form.nome.data.strip()
        email = form.email.data.strip().lower()

        usuario = buscar_por_email(email)

        if usuario:
            flash("E-mail já cadastrado.", "warning")
        else:
            cadastrar_usuario(
                nome,
                email,
                form.senha.data
            )

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("autenticacao.login"))

    return render_template("usuario/cadastro.html", form=form)


@autenticacao_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        usuario = buscar_por_email(email)

        if usuario and verificar_senha(usuario, form.senha.data):
            login_user(usuario)
            return redirect(url_for("principal"))

        flash("E-mail ou senha incorretos.", "danger")

    return render_template("usuario/login.html", form=form)


@autenticacao_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("principal"))