from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(message = "Informe aqui seu e-mail."), Email(message="Digite um e-mail válido."), Length(max = 100)])
    senha = PasswordField("Senha", validators = [DataRequired(message = "Informe aqui sua senha.")])
    entrar = SubmitField("Entrar")