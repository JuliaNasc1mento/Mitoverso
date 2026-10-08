from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class CadastroForm(FlaskForm):
    nome = StringField("Nome", validators = [DataRequired(), Length(max = 150)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    senha = PasswordField("Senha", validators = [DataRequired(), Length(min = 8)])
    confirmar_senha = PasswordField("Confirmar senha", validators = [DataRequired(), EqualTo("senha", message = "As senhas não coindidem")])
    submit = SubmitField("Cadastrar")
