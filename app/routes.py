from app import app
from flask import render_template

# Rota da tela inicial
@app.route("/")
def index():
    return render_template("index.html")

# Rota de tela principal
@app.route("/estude")
def principal():
    return render_template("principal.html")

# Rota da tela do projeto
@app.route("/projeto")
def projeto():
    return render_template("projeto.html")

# Rota da tela dos cards
@app.route("/cards")
def cards():
    return render_template("gameficacao/cards.html")

# Rota da tela de login
@app.route("/login")
def login():
    return render_template("usuario/login.html")