import psycopg2

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hlavni_web():
	return "Toto je hlavni web"

@app.route("/informace")
def informace_web():
	
#ted se zacnu pripojovat do dataaze

	conn = psycopg2.connect(dbname="janicka", user="janicka", password="Toto je tajne heslo", host="da.stderr.cz") #host je dany server

#pomoci cursoru delam to, co chci delat na databazi
	cur1 = conn.cursor()

	cur1.execute("SELECT nazev, kj FROM potraviny;") #timto prikazem vyberu nazev a kj z tabulky potraviny
	tabulka_potravin = cur1.fetchall() #tento prikaz vypise vsechny hodnoty, ktere mam v SELECTU v dane tabulce potraviny

	seznam_potravin = []
	for i in tabulka_potravin:
		seznam_potravin.append("Nazev potraviny: %s , kj (na 1 gram)	: %i" % (i[0], i[1])) #%s mi říká, že chci text a %i, že chci cislo. Za druhym procentem v [] jsou mista, ktere chci v danem seznamu vypsat (na nultem miste je ten nazev a na prvnim je hodnota kj)
	
	return "<br>".join(seznam_potravin)

