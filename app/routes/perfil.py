# Importações
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models.usuario import Usuario
from app.form.perfil_form import PerfilForm
from app.routes.auxiliar import destino_seguro
from app.services.post_service import listar_posts_do_usuario, contar_posts
from app.services.usuario_service import alternar_seguir, atualizar_perfil

# Criação do Blueprint "perfil"
perfil_bp = Blueprint("perfil", __name__)


# /perfil leva para o perfil de quem está logado
@perfil_bp.route("/perfil")
@login_required
def meu_perfil():
    return redirect(url_for("perfil.ver_perfil", id_usuario = current_user.id))


# Rota da tela de perfil de qualquer usuário
@perfil_bp.route("/perfil/<int:id_usuario>")
def ver_perfil(id_usuario):
    usuario = db.get_or_404(Usuario, id_usuario)

    aba = request.args.get("aba", "posts")
    if aba not in ("posts", "respostas", "curtidas"):
        aba = "posts"

    pagina = request.args.get("pagina", 1, type = int)
    paginacao = listar_posts_do_usuario(usuario, aba, pagina)

    return render_template(
        "usuario/perfil.html",
        usuario = usuario,
        aba = aba,
        paginacao = paginacao,
        total_posts = contar_posts(usuario)
    )


@perfil_bp.route("/perfil/editar", methods = ["GET", "POST"])
@login_required
def editar_perfil():
    form = PerfilForm(obj = current_user)

    if form.validate_on_submit():
        atualizar_perfil(current_user, form.nome.data.strip(), (form.bio.data or "").strip())
        flash("Perfil atualizado!", "success")
        return redirect(url_for("perfil.meu_perfil"))

    return render_template("usuario/editar_perfil.html", form = form)


@perfil_bp.route("/perfil/<int:id_usuario>/seguir", methods = ["POST"])
@login_required
def seguir(id_usuario):
    alvo = db.get_or_404(Usuario, id_usuario)

    if alvo.id == current_user.id:
        flash("Você não pode seguir a si mesmo.", "warning")
    else:
        alternar_seguir(current_user, alvo)

    return redirect(destino_seguro(url_for("perfil.ver_perfil", id_usuario = alvo.id)))
