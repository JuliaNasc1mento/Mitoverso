from flask import Flask, render_template
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
app.register_blueprint(autenticacao_bp)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/principal")
def principal():
    return render_template("principal.html")

@app.route("/cards")
def cards():
    return render_template("gameficacao/cards.html")

@app.route("/projeto")
def projeto():
    return render_template("projeto.html")


# Modelos
from app import models
