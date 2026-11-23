from datetime import datetime, timezone
from app import db


class Pergunta(db.Model):
    __tablename__ = "pergunta"

    id = db.Column(db.Integer, primary_key = True)

    # 1 = Fácil, 2 = Médio, 3 = Difícil, 4 = Lendário
    nivel = db.Column(db.Integer, nullable = False, index = True)

    enunciado = db.Column(db.String(300), nullable = False)
    opcao_a = db.Column(db.String(150), nullable = False)
    opcao_b = db.Column(db.String(150), nullable = False)
    opcao_c = db.Column(db.String(150), nullable = False)
    opcao_d = db.Column(db.String(150), nullable = False)

    # Letra da alternativa certa: "A", "B", "C" ou "D"
    correta = db.Column(db.String(1), nullable = False)

    # Texto mostrado depois que o usuário responde
    explicacao = db.Column(db.String(300))

    def opcoes(self):
        return [("A", self.opcao_a), ("B", self.opcao_b), ("C", self.opcao_c), ("D", self.opcao_d)]

    def texto_da_opcao(self, letra):
        return dict(self.opcoes()).get(letra)


class TentativaQuiz(db.Model):
    __tablename__ = "tentativa_quiz"

    id = db.Column(db.Integer, primary_key = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False, index = True)
    nivel = db.Column(db.Integer, nullable = False)
    acertos = db.Column(db.Integer, nullable = False)
    total = db.Column(db.Integer, nullable = False)
    pontos = db.Column(db.Integer, nullable = False)
    criado_em = db.Column(db.DateTime, nullable = False, default = lambda: datetime.now(timezone.utc))

    usuario = db.relationship("Usuario", backref = db.backref("tentativas_quiz", cascade = "all, delete-orphan"))
