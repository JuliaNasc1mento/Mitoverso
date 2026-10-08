# Importações
from flask import Blueprint, render_template

# Criação do Blueprint "login"
autenticacao_bp = Blueprint("autenticacao", __name__)

# Rota da tela de login
@autenticacao_bp.route("/login")
def login():
    return render_template("usuario/login.html")

# Rota da tela de cadastro
@autenticacao_bp.route("/cadastro")
def cadastro():
    return render_template("usuario/cadastro.html")
