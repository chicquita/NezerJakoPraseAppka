#BUDE SLLOUZIT CASEM PRO PRIHLASENI, ZATIM JEN NASTREL

from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
	first_name = StringField('Jméno', validators=[DataRequired("Zadej jméno.")])
	last_name = StringField('Příjmení', validators=[DataRequired("Zadej příjmení.")])
	email = StringField('Email', validators=[DataRequired("Zadej email."), Email("Prosím zadejte emailovou adresu.")])
	password = PasswordField('Heslo', validators=[DataRequired("Zadej heslo."), Length(min=6, message="Heslo musí obsahovat 6 a více znaků.")])
	nickname = StringField('Přezdívka', validators=[DataRequired("Zadej přezdívku.")])
	household = StringField('Domácnost', validators=[DataRequired("Zadej jméno domácnosti.")])
	sex = RadioField('Pohlaví', choices=[('zena','Žena'), ('muz','Muž')])
	age = IntegerField('Věk', validators=[DataRequired("Zadej věk.")])
	weight = IntegerField('Váha (kg)', validators=[DataRequired("Zadej váhu.")])
	height = IntegerField('Výška (cm)', validators=[DataRequired("Zadej výšku.")])
	dailykj = IntegerField('Denní příjem kj', validators=[DataRequired("Zadej denní příjem kj.")])
	makrobilkoviny = IntegerField('Makro bílkoviny (g)', validators=[DataRequired("Zadej makro bílkoviny.")])
	makrosacharidy = IntegerField('Makro sacharidy (g)', validators=[DataRequired("Zadej makro sacharidy.")])
	makrotuky = IntegerField('Makro tuky (g)', validators=[DataRequired("Zadej makro tuky.")])
	submit = SubmitField('Registrovat')
