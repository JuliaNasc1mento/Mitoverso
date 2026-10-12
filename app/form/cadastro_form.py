from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class CadastroForm(FlaskForm):
    nome = StringField("Nome", validators = [DataRequired(message = "Informe aqui seu nome."), Length(max = 100)])
    email = StringField("Email", validators = [DataRequired(message = "Informe aqui seu email."), Email(message = "Digite um email válido."), Length(max = 100)])
    senha = PasswordField("Senha", validators = [DataRequired(message = "Informe aqui sua senha."), Length(min = 8, message = "A senha deve ter no mínimo 8 caracteres.")])
    confirmar_senha = PasswordField("Confirmar senha", validators = [DataRequired(message = "Confirme aqui sua senha."), EqualTo("senha", message = "As senhas não coindidem.")])
    enviar = SubmitField("Cadastrar")
