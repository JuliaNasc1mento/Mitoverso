from app import db

class Mito(db.Model):
    __tablename__ = "mito"

    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(150), nullable = False)
    conteudo = db.Column(db.Text, nullable = False)
    audio = db.Column(db.String(255))