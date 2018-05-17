import psycopg2
import random

def initialize_cursor():
	conn = psycopg2.connect(dbname="janicka", user="janicka", password= "Tajne heslo, ktere neni na githubu", host="da.stderr.cz") #ted se zacnu pripojovat do dataaze
	cur1 = conn.cursor() #pomoci cursoru delam to, co chci delat na databazi
	 
	return cur1

# pro nas hlavni funkce na ktere se budeme odvolavat je select_all, select_single_row a select_single_value
# tyto (a casem) i vice funkci si  muzeme ulozit do balicku, ktery si vzdy importujeme (napr. jako vyse import random) a nemusi nam zbytecne zahlcovat kod

def select_all(select):				# kdyz budes dal psat kod a budes tahat neco selectama, zamysli se, jestli vysledek bude
	cursor = initialize_cursor()		#  1) matice (napr. cela tabulka zasob) - odvolavas se na funkci select_all
	cursor.execute(select)			#  2) jeden radek (napr. select * from zasoby WHERE id = 1) - odvolej se na funkci nize select_single_row
	return cursor.fetchall() 		#  3) nebo pouze 1 hodnota (napr. nize kdyz selectuju denni_prijem_kj), jedna hodnota je prusecikem jednoho radku a jednoho sloupce, odvolej se na funkci select_single_value


def select_single_row(select):
	result_set = select_all(select)
	if not result_set:
		raise Exception ("chces vytahnout 1 hodnotu z DB ale nevrartilo to ani 1 radek")

	return result_set[0] 


def select_single_value(select):
	single_row = select_single_row(select)
	
	return single_row[0]

tabulka_zasob = select_all(
	"SELECT z.id, z.baleni, p.nazev, p.kj, mj.zkratka FROM zasoby z JOIN potraviny p on z.id_potraviny = p.id JOIN merna_jednotka mj on p.id_merna_jednotka = mj.id")
#print (tabulka_zasob)

denni_prijem_kj = select_single_value("SELECT u.denni_prijem_kj FROM uzivatel u WHERE id = 1")
#print(denni_prijem_kj)

kj_potrebne_snidane = int(denni_prijem_kj/100*20)			# doporucene rozlozeni chodu: snidane 20-25%
kj_potrebne_svacina1 = int(denni_prijem_kj/100*10)			# svacina 10-15%
kj_potrebne_obed = int(denni_prijem_kj/100*35)				# obed 30-35%
kj_potrebne_svacina2 = int(denni_prijem_kj/100*15)			# svacina 10-15%
kj_potrebne_vecere = int(denni_prijem_kj/100*20)			# vecere 15-20%


def vyber_jidla(KJ_k_snedku):
	vybrane_kj = 0
	seznam_vybranych_potravin=[]
	tabulka_potravin_pro_funkci = list(tabulka_zasob) #slovo list je zde pridane, protoze bez toho nam to stale chtelo tahat data z prazdne tabulky
	
	while (vybrane_kj < KJ_k_snedku and len(tabulka_potravin_pro_funkci)!=0):
		vybrana_potravina = random.choice(tabulka_potravin_pro_funkci)
		tabulka_potravin_pro_funkci.remove(vybrana_potravina)
		vybrana_potravina_nazev = vybrana_potravina[0]
		vybrana_potravina_kj = vybrana_potravina[1]
		#print(tabulka_zasob)

		if vybrana_potravina_kj <= KJ_k_snedku - vybrane_kj:
			seznam_vybranych_potravin.append(vybrana_potravina)
			#tabulka_potravin.remove(vybrana_potravina) #toto zajisti, ze kdyz ze zasob snim banan na snidani, tak uz se mi nenabidne i na obed, protoze jsem ho snedla
			vybrane_kj = vybrane_kj + vybrana_potravina_kj
			tabulka_zasob.remove(vybrana_potravina)
			print(vybrane_kj)
		
	return (vybrane_kj, seznam_vybranych_potravin)



#tabulka_potravin = filter(lambda x: x[2] not in [13, 40, 67, 68], tabulka_potravin)
#tabulka_potravin = [x for x in tabulka_potravin if x.id_kategorie != 13]
#tabulka_potravin.remove(lambda id_kategorie: id_kategorie not in [13,40,67,68])
SNIDANE = vyber_jidla(kj_potrebne_snidane)
print(SNIDANE)

#tabulka_potravin = list(tabulka_potravin_tmp)
SVACINA1 = vyber_jidla(kj_potrebne_svacina1)
print(SVACINA1)

OBED = vyber_jidla(kj_potrebne_obed)
print (OBED)

SVACINA2 = vyber_jidla(kj_potrebne_svacina2)
print(SVACINA2)

VECERE = vyber_jidla(kj_potrebne_vecere)
print(VECERE)
