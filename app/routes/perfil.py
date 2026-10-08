# Importações
from flask import Blueprint, render_template

# Criação do Blueprint "perfil"
perfil_bp = Blueprint("perfil", __name__)

# Rota da tela de perfil
@perfil_bp.routes("/perfil")
def perfil():
    return render_template("usuario/perfil.html")
