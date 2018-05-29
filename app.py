from flask import Flask, render_template, request, redirect, url_for
from flask_table import Table, Col
import psycopg2
from polozka_jidelnicku import Polozka_jidelnicku
from dbHelper import DbHelper
from baseVypocet import BaseVypocet         #baseVypocet obsahuje testovaci hodnoty pro jidelnicek
from vypocetDbBased import vypocetDbBased    
'''vypocetDbBased: generovani jidelnicku zalozeno na selectech z DB 
(DB pracuje navic s tabulkami pattern, pattern_line, pattern_line_set) narozdil od vypoctu zalozenem na pythonu'''

'''from forms import SignupForm
   registrace a propisovani dat do db se bude resit az v budoucnu'''

#---------------------------------------------------------PRIPOJENI DO DB & SELECTY ------------------------------------------------------------#

DB = DbHelper("ada", "ada", "To heslo ti nereknu")               
#v DBHelperu je obsazeno napojeni do DB a zakladni selecty (select_all,single row, single value)

VYPOCET = VypocetDbBased()        #sem se hodi nazev jancinyho filu s vypoctem

app = Flask(__name__)

#-------------------------------------------------------------------HOMEPAGE--------------------------------------------------------------------#
@app.route("/")
def index():
  return render_template("index.html")

#----------------------------------------------------------------JIDELNICEK.HTML----------------------------------------------------------------#
#-------------------OBJEKTY A FUNKCE PRO JIDELNICEK--------------
SNIDANE_ID = 1
SVACINA_DOPO_ID = 2
OBED_ID = 3
SVACINA_ODPO_ID = 4
VECERE_ID = 5

def get_snidane():
  #return BaseVypocet.get_snidane()
  return VYPOCET.get_snidane()

#pro ostatni funkce poucivam prozatim testovaci hodnoty z BaseVypocet(tam jsou polozky jidelnicku napsany natvrdo v kodu, nejsou tahane z DB)
def get_svacina_dopo():
    return BaseVypocet.get_svacina_dopo()
              
def get_obed():
  return BaseVypocet.get_obed()

def get_svacina_odpo():
  return BaseVypocet.get_svacina_odpo()

def get_vecere():
  return BaseVypocet.get_vecere()


#------------------------JIDELNICEK HTML-----------------------
@app.route("/jidelnicek", methods=['GET', 'POST'])
def jidelnicek():
  if request.method=='POST':
    zobrazJidelnicek = "initial"
    '''podminka znamena, ze pokud uzivatel appky na webu jidelnicek.html zmacne tlacitko "generuj", jidelnicek se zobrazi, pokud 
    tlacitko zmackle neni, zobrazi se pouze tabulka s volbou chodu'''
  else:
    zobrazJidelnicek = "None"

  if request.method=='POST':
    is_snidane = request.form.get('is_snidane', False)
    is_svacina_dopo = request.form.get('is_svacina_dopo', False)
    is_obed = request.form.get('is_obed', False)
    is_svacina_odpo = request.form.get('is_svacina_odpo', False)
    is_vecere = request.form.get('is_vecere', False)
    ''' podobne jako u zobrazeni jidelnicku, pokud uzivatel zatrhne checkbox ze dany chod chce, tak se ten chod vyprintuje na html, 
        chody, ktere zaskrtnute nejsou se nezobrazi'''
  else:
    is_snidane = False
    is_svacina_dopo = False
    is_obed = False
    is_svacina_odpo = False
    is_vecere = False

  class Jidelnicek(Table):
    nazev = Col('Název')
    mnozstvi = Col('Množství')
    '''urcuji vystup, ktery budeme zobrazovat, jak pro jidelnicek, tak i tabulku zasob,
     prozatim jsem zvolila nazev a mnozstvi (mnozstvi v sobe spojuje hodnotu mnozstvi a merne jednotky)
     mozne v budoucnu doplnit o kj, prozatim staci'''

 # populuji tabulku pro kazdy z chodu
  tabulka_jidelnicek_snidane = Jidelnicek(get_snidane())
  tabulka_jidelnicek_svacina_dopo = Jidelnicek(get_svacina_dopo())
  tabulka_jidelnicek_obed = Jidelnicek(get_obed())
  tabulka_jidelnicek_svacina_odpo = Jidelnicek(get_svacina_odpo())
  tabulka_jidelnicek_vecere = Jidelnicek(get_vecere())

  #vyprintovani html
  return render_template("jidelnicek.html",
    zobrazJidelnicek = zobrazJidelnicek,
    zobrazSnidane = "initial" if is_snidane else "None",
    zobrazSvacinaDopo = "initial" if is_svacina_dopo else "None",
    zobrazObed = "initial" if is_obed else "None",
    zobrazSvacinaOdpo = "initial" if is_svacina_odpo else "None",
    zobrazVecere = "initial" if is_vecere else "None", 
    jidelnicek_snidane = tabulka_jidelnicek_snidane.__html__(), 
    jidelnicek_svacina_dopo = tabulka_jidelnicek_svacina_dopo.__html__(), 
    jidelnicek_obed = tabulka_jidelnicek_obed.__html__(),  
    jidelnicek_svacina_odpo = tabulka_jidelnicek_svacina_odpo.__html__(), 
    jidelnicek_vecere = tabulka_jidelnicek_vecere.__html__()
    )


#-------------------------------------------------------------------ZASOBY---------------------------------------------------------------#

@app.route("/zasoby")
def zasoby():
  class Tabulka_zasob(Table):
    nazev = Col('Název')
    mnozstvi = Col('Množství')

  class Zasoba(object):
    def __init__(self, nazev, mnozstvi):
        self.nazev = nazev
        self.mnozstvi = mnozstvi

  #slouzi pro razeni zasob dle abecedy
  def sort_zasoby(item):
        return item[0] 

  def get_zasoby():
    zasoby_z_db = DB.select_all("SELECT p.nazev, z.baleni, mj.zkratka FROM zasoby z JOIN potraviny p on z.id_potraviny = p.id JOIN merna_jednotka mj on p.id_merna_jednotka = mj.id")
    zasoby = []
    zasoby_z_db_sorted = sorted(zasoby_z_db, key=sort_zasoby)                    
    for tuple in zasoby_z_db_sorted:
      zasoby.append(Zasoba(tuple[0],str(tuple[1]) +" "+ tuple[2]))

    return zasoby

  # Populate the table
  tabulka_zasob = Tabulka_zasob(get_zasoby())

  # Print the html
  return render_template("zasoby.html", tabulka_zasob = tabulka_zasob.__html__())
#-------------------------------------------------------------------MUJ UCET---------------------------------------------------------------#

'''
TATO STRANKA JE JESTE VE VYSTAVBE(viz problem s query nize), SLUCUJE JIDELNICEK.HTML a ZASOBY.HTML DOHROMADY, 
BUDE UMOZNOVAT I ZADAVANI POTRAVIN DO DB
'''

@app.route("/muj_ucet", methods=['GET', 'POST'])
def muj_ucet():
  if request.method=='POST':
    hodnotaParametruQuery = request.form['query']
    ''' toto se tyka sekce, kam si uzivatel muze vlozit potravinu do DB
    'query' oznacuje pole, kam se potravina pise, opet zalozeno na metode post - tedy pracuji s vstupem od uzivatele az ve chvili,
    kdyz zmackne policko hledej, v opacnem pripade vraci defaultni hodnotu
    TOTO JE JESTE VE VYSTAVBE!
    DELA PROBLEMY KDYZ CHCI GENEROVAT JIDELNICEK PRIMO NA mujucet.html, PROTO MAM JIDELNICEK ZATIM BOKEM NA VLASTNI HTML STRANCE'''

  else:
    hodnotaParametruQuery = request.args.get('parameter1', 'default value')


  class Tabulka_zasob(Table):
    nazev = Col('Název')
    mnozstvi = Col('Množství')
    
  # Get some objects
  class Zasoba(object):
    def __init__(self, nazev, mnozstvi):
        self.nazev = nazev
        self.mnozstvi = mnozstvi

  #slouzi pro razeni zasob dle abecedy
  def sort_zasoby(item):
        return item[0]  

  def get_zasoby():
    zasoby_z_db = DB.select_all("SELECT p.nazev, z.baleni, mj.zkratka FROM zasoby z JOIN potraviny p on z.id_potraviny = p.id JOIN merna_jednotka mj on p.id_merna_jednotka = mj.id")
    zasoby = []
    zasoby_z_db_sorted = sorted(zasoby_z_db, key=sort_zasoby)                    
    for tuple in zasoby_z_db_sorted:
      zasoby.append(Zasoba(tuple[0],str(tuple[1]) +" "+ tuple[2]))

    return zasoby

  # Populate the table
  tabulka_zasob = Tabulka_zasob(get_zasoby())

  # Print the html
  print(tabulka_zasob.__html__())
  # or just {{ table }} from within a Jinja template


  #----------------------------------------------
  if request.method=='POST':
    zobrazJidelnicek = "initial"
  else:
    zobrazJidelnicek = "None"

  if request.method=='POST':
    is_snidane = request.form.get('is_snidane', False)
    is_svacina_dopo = request.form.get('is_svacina_dopo', False)
    is_obed = request.form.get('is_obed', False)
    is_svacina_odpo = request.form.get('is_svacina_odpo', False)
    is_vecere = request.form.get('is_vecere', False)
  else:
    is_snidane = False
    is_svacina_dopo = False
    is_obed = False
    is_svacina_odpo = False
    is_vecere = False

  class Jidelnicek(Table):
    nazev = Col('Název')
    mnozstvi = Col('Množství')

 # Populate the table
  tabulka_jidelnicek_snidane = Jidelnicek(get_snidane())
  tabulka_jidelnicek_svacina_dopo = Jidelnicek(get_svacina_dopo())
  tabulka_jidelnicek_obed = Jidelnicek(get_obed())
  tabulka_jidelnicek_svacina_odpo = Jidelnicek(get_svacina_odpo())
  tabulka_jidelnicek_vecere = Jidelnicek(get_vecere())

  # Print the html
  return render_template("muj_ucet.html", 
    hodnotaParametruQuery = hodnotaParametruQuery, 
    tabulka_zasob = tabulka_zasob.__html__(),
    zobrazJidelnicek = zobrazJidelnicek,
    zobrazSnidane = "initial" if is_snidane else "None",
    zobrazSvacinaDopo = "initial" if is_svacina_dopo else "None",
    zobrazObed = "initial" if is_obed else "None",
    zobrazSvacinaOdpo = "initial" if is_svacina_odpo else "None",
    zobrazVecere = "initial" if is_vecere else "None", 
    jidelnicek_snidane = tabulka_jidelnicek_snidane.__html__(), 
    jidelnicek_svacina_dopo = tabulka_jidelnicek_svacina_dopo.__html__(), 
    jidelnicek_obed = tabulka_jidelnicek_obed.__html__(),  
    jidelnicek_svacina_odpo = tabulka_jidelnicek_svacina_odpo.__html__(), 
    jidelnicek_vecere = tabulka_jidelnicek_vecere.__html__()
    )





#-------------------------------------------------------------------REGISTRACE---------------------------------------------------------------#

# KOD JE POUZE NASTREL, ZATIM NEFUNGUJE, NEMA VYSOKOU PRIORITU

@app.route("/signup", methods=['GET', 'POST'])
def signup():
  error = None
  if request.method == 'POST':
      if request.form['prezdivka'] != 'admin' or request.form['heslo'] != 'admin':
        error = 'Neplatné přihlašovací údaje. Prosím zkuste znovu.'
      else:
        return redirect(url_for('/'))
  return render_template('signup.html', error=error)

'''
@app.route("/signup", methods=["GET", "POST"])
def signup():
  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      return 'Success!'

  elif request.method == "GET":
    return render_template('signup.html', form=form)

'''

#-------------------------------------------------------------------ELEMENTS---------------------------------------------------------------#

#NA TETO STRANCE MAM VZORY RUZNYCH TYPU TLACITEK, TABULEK, SLOUZI POUZE PRO VYSTAVBU HTML

@app.route("/elements")
def elements():
  return render_template("elements.html")

if __name__ == "__main__":
  app.run(debug=True)



#------------------------------------------------------------UZITECNY VYGOOGLENY KOD--------------------------------------------------------#
'''
---------------------------LOGIN----------------------------
<html>
  <head>
    <title>Flask Intro - login page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="static/bootstrap.min.css" rel="stylesheet" media="screen">
  </head>
  <body>
    <div class="container">
      <h1>Please login</h1>
      <br>
      <form action="" method="post">
        <input type="text" placeholder="Username" name="username" value="{{
          request.form.username }}">
         <input type="password" placeholder="Password" name="password" value="{{
          request.form.password }}">
        <input class="btn btn-default" type="submit" value="Login">
      </form>
      {% if error %}
        <p class="error"><strong>Error:</strong> {{ error }}
      {% endif %}
    </div>
  </body>
</html>
'''



#https://pythonspot.com/flask-web-forms/
#http://flask.pocoo.org/docs/1.0/quickstart/