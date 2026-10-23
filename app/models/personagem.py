from app import db

class Personagem(db.Model):
    __tablename__ = "personagem"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    categoria = db.Column(db.String(30), nullable = False)
    descricao = db.Column(db.Text, nullable = False)
    imagem = db.Column(db.String(255), nullable = False)

    id_pai = db.Column(db.Integer, db.ForeignKey("personagem.id"), nullable = True)
    id_mae = db.Column(db.Integer, db.ForeignKey("personagem.id"), nullable = True)

    pai = db.relationship("Personagem", foreign_keys = [id_pai], remote_side = [id], uselist = False)
    mae = db.relationship("Personagem", foreign_keys = [id_mae], remote_side = [id], uselist = False)
