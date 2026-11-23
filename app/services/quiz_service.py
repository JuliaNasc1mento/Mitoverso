from app import db
from app.models.usuario import Usuario
from app.models.quiz import Pergunta, TentativaQuiz

QUESTOES_POR_QUIZ = 5
LIMITE_RANKING = 20

# Pontos por acerto em cada nível: quanto mais difícil, mais vale
NIVEIS = {
    1: {"nome": "Fácil",    "pontos": 10, "icone": "bi-star"},
    2: {"nome": "Médio",    "pontos": 20, "icone": "bi-lightning-charge"},
    3: {"nome": "Difícil",  "pontos": 30, "icone": "bi-fire"},
    4: {"nome": "Lendário", "pontos": 40, "icone": "bi-gem"},
}


def sortear_perguntas(nivel):
    consulta = (
        db.select(Pergunta)
        .where(Pergunta.nivel == nivel)
        .order_by(db.func.random())
        .limit(QUESTOES_POR_QUIZ)
    )
    return db.session.scalars(consulta).all()


def corrigir(ids, respostas):
    # ids = perguntas que foram sorteadas / respostas = {id_pergunta: letra marcada}
    perguntas = db.session.scalars(db.select(Pergunta).where(Pergunta.id.in_(ids))).all()
    por_id = {p.id: p for p in perguntas}

    itens = []
    acertos = 0

    for id_pergunta in ids:
        pergunta = por_id.get(id_pergunta)
        if not pergunta:
            continue

        marcada = respostas.get(id_pergunta)
        acertou = marcada == pergunta.correta
        if acertou:
            acertos += 1

        itens.append({"pergunta": pergunta, "marcada": marcada, "acertou": acertou})

    return itens, acertos


def registrar_tentativa(usuario, nivel, acertos, total):
    pontos = acertos * NIVEIS[nivel]["pontos"]

    tentativa = TentativaQuiz(
        id_usuario = usuario.id,
        nivel = nivel,
        acertos = acertos,
        total = total,
        pontos = pontos
    )
    db.session.add(tentativa)
    db.session.commit()

    return tentativa


def melhores_por_nivel(usuario):
    linhas = db.session.execute(
        db.select(TentativaQuiz.nivel, db.func.max(TentativaQuiz.pontos))
        .where(TentativaQuiz.id_usuario == usuario.id)
        .group_by(TentativaQuiz.nivel)
    ).all()

    return {nivel: pontos for nivel, pontos in linhas}


def ranking_completo():
    # Só a MELHOR pontuação de cada usuário em cada nível conta.
    # Assim, repetir o mesmo quiz várias vezes não infla o ranking.
    melhores = (
        db.select(
            TentativaQuiz.id_usuario,
            TentativaQuiz.nivel,
            db.func.max(TentativaQuiz.pontos).label("pontos")
        )
        .group_by(TentativaQuiz.id_usuario, TentativaQuiz.nivel)
        .subquery()
    )

    total = db.func.sum(melhores.c.pontos)

    consulta = (
        db.select(Usuario, total.label("total"), db.func.count(melhores.c.nivel).label("niveis"))
        .join(melhores, melhores.c.id_usuario == Usuario.id)
        .group_by(Usuario.id)
        .order_by(total.desc(), Usuario.id)
    )

    # Cada linha: (usuario, pontos totais, quantidade de níveis jogados)
    return db.session.execute(consulta).all()
