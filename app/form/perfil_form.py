from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class PerfilForm(FlaskForm):
    nome = StringField("Nome", validators = [DataRequired(message = "Informe aqui seu nome."), Length(max = 100)])
    bio = TextAreaField("Bio", validators = [Optional(), Length(max = 200, message = "A bio pode ter no máximo 200 caracteres.")])
    enviar = SubmitField("Salvar")
