from datetime import datetime, timezone
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

# Aplicação
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
csrf.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "autenticacao.login"

# Rotas
from app.routes.autenticacao import autenticacao_bp
from app.routes.perfil import perfil_bp
from app.routes.posts import posts_bp
app.register_blueprint(autenticacao_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(posts_bp)

from app.models.mito import Mito

# Filtro para mostrar "há quanto tempo" um post foi publicado
@app.template_filter("tempo_atras")
def tempo_atras(data):
    if not data:
        return ""

    if data.tzinfo is None:
        data = data.replace(tzinfo = timezone.utc)

    segundos = int((datetime.now(timezone.utc) - data).total_seconds())

    if segundos < 60:
        return "agora"
    if segundos < 3600:
        return f"{segundos // 60} min"
    if segundos < 86400:
        return f"{segundos // 3600} h"
    if segundos < 604800:
        return f"{segundos // 86400} d"
    return data.strftime("%d/%m/%Y")

# Gera o link de outra página mantendo a aba e os outros parâmetros da URL atual
@app.template_global()
def url_pagina(numero):
    argumentos = {**(request.view_args or {}), **request.args.to_dict(), "pagina": numero}
    return url_for(request.endpoint, **argumentos)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/principal")
def principal():
    mitos = Mito.query.order_by(Mito.id.asc()).all()
    return render_template("principal.html", mitos = mitos)

@app.route("/mito/<int:mito_id>")
def detalhes_mito(mito_id):
    mito = Mito.query.get_or_404(mito_id)

    return render_template("mito.html", mito = mito)

@app.route("/cards")
def cards():
    return render_template("gameficacao/cards.html")

@app.route("/projeto")
def projeto():
    return render_template("projeto.html")

# Rotas da pasta cards de personagens
@app.route("/deuses")
def deuses():
    return render_template("gameficacao/deusescards.html")

@app.route("/espiritos")
def espiritos():
    return render_template("gameficacao/espiritoscards.html")

@app.route("/herois")
def herois():
    return render_template("gameficacao/heroiscards.html")

@app.route("/monstros")
def monstros():
    return render_template("gameficacao/monstroscards.html")

@app.route("/primordiais")
def primordiais():
    return render_template("gameficacao/primordiaiscards.html")

@app.route("/titas")
def titas():
    return render_template("gameficacao/titascards.html")

# Modelos
from app import models

#Quiz
from app.routes.quiz import quiz_bp
app.register_blueprint(quiz_bp)