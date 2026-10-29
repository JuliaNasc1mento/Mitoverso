from app import db

class Curtida(db.Model):
    __tablename__ = "curtida"

    id = db.Column(db.Integer, primary_key = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)
    id_post = db.Column(db.Integer, db.ForeignKey("post.id"), nullable = False)

    # Cada usuário só pode curtir o mesmo post uma vez
    __table_args__ = (db.UniqueConstraint("id_usuario", "id_post", name = "uq_curtida_usuario_post"),)
