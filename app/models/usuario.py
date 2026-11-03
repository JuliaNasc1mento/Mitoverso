from datetime import datetime, timezone
from app import db
from flask_login import UserMixin

# Tabela de associação: quem segue quem (muitos-para-muitos entre usuários)
seguidor = db.Table(
    "seguidor",
    db.Column("id_seguidor", db.Integer, db.ForeignKey("usuario.id"), primary_key = True),
    db.Column("id_seguido", db.Integer, db.ForeignKey("usuario.id"), primary_key = True)
)

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    senha = db.Column(db.String(256), nullable = False)
    bio = db.Column(db.String(200))
    criado_em = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    # usuario.seguindo -> quem eu sigo / usuario.seguidores -> quem me segue
    seguindo = db.relationship(
        "Usuario",
        secondary = seguidor,
        primaryjoin = (seguidor.c.id_seguidor == id),
        secondaryjoin = (seguidor.c.id_seguido == id),
        backref = "seguidores"
    )
