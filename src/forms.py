from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired

class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class UploadForm(FlaskForm):
    class Meta:
        csrf = False

    title = StringField('Título', validators=[DataRequired(), Length(min=1, max=250)])
    author = StringField('Autor', validators=[DataRequired(), Length(min=1, max=250)])
    cover = FileField('Portada', validators=[FileRequired()])
    submit = SubmitField('Subir')
