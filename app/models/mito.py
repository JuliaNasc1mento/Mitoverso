from app import db

class Mito(db.Model):
    __tablename__ = "mito"

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(150), nullable = False)
    resumo = db.Column(db.String(300), nullable = False)
    conteudo = db.Column(db.Text, nullable = False)
    imagem = db.Column(db.String(255))
    audio = db.Column(db.String(255))