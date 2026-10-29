from datetime import datetime, timezone
from app import db

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key = True)
    conteudo = db.Column(db.Text, nullable = False)
    criado_em = db.Column(db.DateTime, nullable = False, default = lambda: datetime.now(timezone.utc))

    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)

    # Se id_pai for None, é um post normal. Se tiver valor, é uma resposta a outro post.
    id_pai = db.Column(db.Integer, db.ForeignKey("post.id"), nullable = True)

    autor = db.relationship("Usuario", backref = db.backref("posts", cascade = "all, delete-orphan"))

    respostas = db.relationship(
        "Post",
        backref = db.backref("pai", remote_side = [id]),
        cascade = "all, delete-orphan",
        order_by = "Post.criado_em"
    )

    curtidas = db.relationship("Curtida", backref = "post", cascade = "all, delete-orphan")

    def curtido_por(self, usuario):
        if not usuario.is_authenticated:
            return False
        return any(c.id_usuario == usuario.id for c in self.curtidas)
