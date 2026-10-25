from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key = True)
    conteudo = db.Column(db.Text, nullable = False)
    data_criacao = db.Column(db.DateTime, nullable = False, default = datetime.now)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)

