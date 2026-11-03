from urllib.parse import urlparse
from flask import request


def destino_seguro(padrao):
    # Lê o parâmetro "next" (do formulário ou da URL) e só aceita caminhos internos do site
    destino = request.values.get("next", "")

    if (
        destino.startswith("/")
        and not destino.startswith("//")
        and "\\" not in destino
        and not urlparse(destino).netloc
    ):
        return destino

    return padrao
