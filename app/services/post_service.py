from app import db
from app.models.post import Post
from app.models.curtida import Curtida

POSTS_POR_PAGINA = 10


def criar_post(usuario, conteudo, id_pai = None):
    post = Post(conteudo = conteudo, id_usuario = usuario.id, id_pai = id_pai)
    db.session.add(post)
    db.session.commit()

    return post


def excluir_post(post):
    db.session.delete(post)
    db.session.commit()


def alternar_curtida(usuario, post):
    # Retorna True se curtiu e False se descurtiu
    curtida = db.session.scalar(
        db.select(Curtida).filter_by(id_usuario = usuario.id, id_post = post.id)
    )

    if curtida:
        db.session.delete(curtida)
        db.session.commit()
        return False

    db.session.add(Curtida(id_usuario = usuario.id, id_post = post.id))
    db.session.commit()
    return True


def _paginar(consulta, pagina):
    return db.paginate(consulta, page = pagina, per_page = POSTS_POR_PAGINA, error_out = False)


def listar_feed(pagina):
    consulta = db.select(Post).where(Post.id_pai.is_(None)).order_by(Post.criado_em.desc())
    return _paginar(consulta, pagina)


def listar_feed_seguindo(usuario, pagina):
    ids = [u.id for u in usuario.seguindo] + [usuario.id]
    consulta = (
        db.select(Post)
        .where(Post.id_pai.is_(None), Post.id_usuario.in_(ids))
        .order_by(Post.criado_em.desc())
    )
    return _paginar(consulta, pagina)


def listar_posts_do_usuario(usuario, aba, pagina):
    if aba == "respostas":
        consulta = (
            db.select(Post)
            .where(Post.id_usuario == usuario.id, Post.id_pai.is_not(None))
            .order_by(Post.criado_em.desc())
        )
    elif aba == "curtidas":
        consulta = (
            db.select(Post)
            .join(Curtida, Curtida.id_post == Post.id)
            .where(Curtida.id_usuario == usuario.id)
            .order_by(Curtida.id.desc())
        )
    else:
        consulta = (
            db.select(Post)
            .where(Post.id_usuario == usuario.id, Post.id_pai.is_(None))
            .order_by(Post.criado_em.desc())
        )

    return _paginar(consulta, pagina)


def contar_posts(usuario):
    return db.session.scalar(
        db.select(db.func.count()).select_from(Post)
        .where(Post.id_usuario == usuario.id, Post.id_pai.is_(None))
    )
