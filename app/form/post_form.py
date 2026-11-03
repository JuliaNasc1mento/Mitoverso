from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    conteudo = TextAreaField(
        "Conteúdo",
        validators = [
            DataRequired(message = "Escreva algo antes de publicar."),
            Length(max = 500, message = "O post pode ter no máximo 500 caracteres.")
        ]
    )
    enviar = SubmitField("Publicar")
