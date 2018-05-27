import psycopg2

from flask import Flask, render_template

app = Flask(__name__)

def selecty_z_databaze(select):
	conn = psycopg2.connect(dbname="janicka", user="janicka", password="Toto je tajne heslo", host="da.stderr.cz") #ted se zacnu pripojovat do dataaze
	cur1 = conn.cursor() #pomoci cursoru delam to, co chci delat na databazi

	cur1.execute(select) 
	return cur1.fetchall() #tento prikaz vypise vsechny hodnoty, ktere mam v selectu v dane tabulce

@app.route("/")
def hlavni_web():
	return "Toto je hlavni web"

@app.route("/informace")
def informace_web():
	tabulka_potravin = selecty_z_databaze("SELECT nazev, kj FROM potraviny;") #timto prikazem vyberu vsechno z tabulky potraviny
	
	seznam_potravin = []
	for i in tabulka_potravin:
		seznam_potravin.append("Nazev potraviny: %s , kj (na 1 gram)	: %i" % (i[0], i[1])) #%s mi říká, že chci text a %i, že chci cislo. Za druhym procentem v [] jsou mista, ktere chci v danem seznamu vypsat (na nultem miste je ten nazev a na prvnim je hodnota kj)
	
	return "<br>".join(seznam_potravin)

@app.route("/vyberPotravin")
def vyberPotravin_web():
	vyberPotravin = selecty_z_databaze("SELECT nazev FROM potraviny")

@app.route('/test')
@app.route('/test/<kocicka>')
def hello(kocicka=None):
	return render_template('hlavni.html', name=kocicka)

