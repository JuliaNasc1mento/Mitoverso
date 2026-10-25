import os

from flask import (Blueprint, render_template, request, redirect, url_for, flash, current_app)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models.post import Post

perfil_bp = Blueprint("perfil", __name__)

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "webp"}

@perfil_bp.route("/perfil")
@login_required
def perfil():
    meus_posts = Post.query.filter_by(
        usuario_id=current_user.id
    ).order_by(
        Post.data_criacao.desc()
    ).all()

    return render_template(
        "usuario/perfil.html",
        meus_posts=meus_posts
    )

@perfil_bp.route("/perfil/publicar", methods=["POST"])
@login_required
def publicar():
    conteudo = request.form.get("conteudo", "").strip()

    if not conteudo:
        flash("Escreva algo antes de publicar.", "warning")
        return redirect(url_for("perfil.perfil"))

    novo_post = Post(
        conteudo=conteudo,
        usuario_id=current_user.id
    )

    db.session.add(novo_post)
    db.session.commit()

    flash("Publicação criada com sucesso!", "success")
    return redirect(url_for("perfil.perfil"))


@perfil_bp.route("/perfil/foto", methods=["POST"])
@login_required
def atualizar_foto():
    arquivo = request.files.get("foto")

    if not arquivo or not arquivo.filename:
        flash("Selecione uma imagem.", "warning")
        return redirect(url_for("perfil.perfil"))

    nome_original = secure_filename(arquivo.filename)

    if (
        "." not in nome_original
        or nome_original.rsplit(".", 1)[1].lower()
        not in EXTENSOES_PERMITIDAS
    ):
        flash("Formato de imagem não permitido.", "danger")
        return redirect(url_for("perfil.perfil"))

    extensao = nome_original.rsplit(".", 1)[1].lower()
    nome_arquivo = f"usuario_{current_user.id}.{extensao}"

    pasta_perfis = os.path.join(
        current_app.static_folder, "img", "perfis"
    )
    os.makedirs(pasta_perfis, exist_ok=True)

    caminho = os.path.join(pasta_perfis, nome_arquivo)
    arquivo.save(caminho)

    current_user.foto_perfil = f"img/perfis/{nome_arquivo}"
    db.session.commit()

    flash("Foto de perfil atualizada!", "success")
    return redirect(url_for("perfil.perfil"))
