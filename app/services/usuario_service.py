from app.database import db
from app.models import Usuario
from werkzeug.security import (generate_password_hash, check_password_hash)

def buscar_por_email(email):
    return Usuario.query.filter_by(email = email).first()

def cadastrar_usuario(nome, email, senha):
    senha_hash = generate_password_hash(senha)
    usuario = Usuario(nome = nome, email = email, senha = senha_hash)
    db.session.add(usuario)
    db.session.commit()
    return usuario

def verificar_senha(usuario, senha):
    return check_password_hash(usuario.senha, senha)



