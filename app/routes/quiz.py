import click
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_required, current_user

from app.services.quiz_seed import cadastrar_perguntas_iniciais
from app.services.quiz_service import (
    NIVEIS,
    QUESTOES_POR_QUIZ,
    LIMITE_RANKING,
    sortear_perguntas,
    corrigir,
    registrar_tentativa,
    melhores_por_nivel,
    ranking_completo
)

quiz_bp = Blueprint("quiz", __name__)


# Comando de terminal: flask quiz seed
@quiz_bp.cli.command("seed")
def seed():
    """Cadastra as perguntas iniciais do quiz."""
    novas = cadastrar_perguntas_iniciais()
    click.echo(f"{novas} pergunta(s) nova(s) cadastrada(s).")


# Página inicial do quiz: escolha do nível
@quiz_bp.route("/quiz")
def index():
    melhores = melhores_por_nivel(current_user) if current_user.is_authenticated else {}
    return render_template("quiz/index.html", niveis = NIVEIS, melhores = melhores, questoes = QUESTOES_POR_QUIZ)


# Sorteia as perguntas do nível e mostra o quiz
@quiz_bp.route("/quiz/<int:nivel>")
@login_required
def jogar(nivel):
    if nivel not in NIVEIS:
        abort(404)

    perguntas = sortear_perguntas(nivel)
    if not perguntas:
        flash("Ainda não há perguntas neste nível.", "warning")
        return redirect(url_for("quiz.index"))

    # Guarda na sessão quais perguntas foram sorteadas, para corrigir só essas
    session[f"quiz_{nivel}"] = [p.id for p in perguntas]

    return render_template("quiz/jogar.html", nivel = nivel, info = NIVEIS[nivel], perguntas = perguntas)


# Recebe as respostas, corrige e salva a pontuação
@quiz_bp.route("/quiz/<int:nivel>/enviar", methods = ["POST"])
@login_required
def enviar(nivel):
    if nivel not in NIVEIS:
        abort(404)

    # pop: cada quiz sorteado só pode ser enviado uma vez (evita pontuar duas vezes ao atualizar a página)
    ids = session.pop(f"quiz_{nivel}", None)
    if not ids:
        flash("Esse quiz expirou. Comece uma nova rodada.", "warning")
        return redirect(url_for("quiz.index"))

    respostas = {id_pergunta: request.form.get(f"pergunta_{id_pergunta}") for id_pergunta in ids}
    itens, acertos = corrigir(ids, respostas)

    recorde_anterior = melhores_por_nivel(current_user).get(nivel, 0)
    tentativa = registrar_tentativa(current_user, nivel, acertos, len(itens))

    return render_template(
        "quiz/resultado.html",
        nivel = nivel,
        info = NIVEIS[nivel],
        itens = itens,
        tentativa = tentativa,
        novo_recorde = tentativa.pontos > recorde_anterior,
        ultimo_nivel = max(NIVEIS)
    )


# Ranking de usuários
@quiz_bp.route("/quiz/ranking")
def ranking():
    todos = ranking_completo()

    minha_posicao = None
    meus_pontos = 0
    if current_user.is_authenticated:
        for posicao, (usuario, pontos, niveis) in enumerate(todos, start = 1):
            if usuario.id == current_user.id:
                minha_posicao = posicao
                meus_pontos = pontos
                break

    return render_template(
        "quiz/ranking.html",
        top = todos[:LIMITE_RANKING],
        limite = LIMITE_RANKING,
        minha_posicao = minha_posicao,
        meus_pontos = meus_pontos,
        total_niveis = len(NIVEIS),
        pontos_maximos = sum(n["pontos"] for n in NIVEIS.values()) * QUESTOES_POR_QUIZ
    )
