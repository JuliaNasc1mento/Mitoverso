from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app import db
from app.models.post import Post
from app.form.post_form import PostForm
from app.routes.auxiliar import destino_seguro
from app.services.post_service import (
    criar_post,
    excluir_post,
    alternar_curtida,
    listar_feed,
    listar_feed_seguindo
)

posts_bp = Blueprint("posts", __name__)


def _flash_erros(form):
    for erros in form.errors.values():
        for erro in erros:
            flash(erro, "danger")


# Página do fórum (feed)
@posts_bp.route("/posts")
def feed():
    aba = request.args.get("aba", "todos")
    pagina = request.args.get("pagina", 1, type = int)

    if aba == "seguindo" and current_user.is_authenticated:
        paginacao = listar_feed_seguindo(current_user, pagina)
    else:
        aba = "todos"
        paginacao = listar_feed(pagina)

    return render_template("usuario/post.html", form = PostForm(), paginacao = paginacao, aba = aba)


# Página de um post com as respostas
@posts_bp.route("/posts/<int:id_post>")
def ver_post(id_post):
    post = db.get_or_404(Post, id_post)
    return render_template("usuario/post_detalhe.html", post = post, form = PostForm())


@posts_bp.route("/posts/novo", methods = ["POST"])
@login_required
def novo_post():
    form = PostForm()

    if form.validate_on_submit():
        criar_post(current_user, form.conteudo.data.strip())
        flash("Post publicado!", "success")
    else:
        _flash_erros(form)

    return redirect(url_for("posts.feed"))


@posts_bp.route("/posts/<int:id_post>/responder", methods = ["POST"])
@login_required
def responder(id_post):
    post = db.get_or_404(Post, id_post)
    form = PostForm()

    if form.validate_on_submit():
        criar_post(current_user, form.conteudo.data.strip(), id_pai = post.id)
        flash("Resposta publicada!", "success")
    else:
        _flash_erros(form)

    return redirect(url_for("posts.ver_post", id_post = post.id))


@posts_bp.route("/posts/<int:id_post>/curtir", methods = ["POST"])
@login_required
def curtir(id_post):
    post = db.get_or_404(Post, id_post)
    alternar_curtida(current_user, post)

    return redirect(destino_seguro(url_for("posts.ver_post", id_post = post.id)))


@posts_bp.route("/posts/<int:id_post>/excluir", methods = ["POST"])
@login_required
def excluir(id_post):
    post = db.get_or_404(Post, id_post)

    # Só o autor pode apagar o próprio post
    if post.id_usuario != current_user.id:
        abort(403)

    id_pai = post.id_pai
    excluir_post(post)
    flash("Post excluído.", "info")

    if id_pai:
        return redirect(url_for("posts.ver_post", id_post = id_pai))
    return redirect(url_for("posts.feed"))
