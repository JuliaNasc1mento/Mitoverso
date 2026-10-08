from app import db

class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    senha = db.Column(db.String(255), nullable = False)
    