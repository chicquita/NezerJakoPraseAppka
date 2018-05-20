# Prvně si potřebuju určit, které potraviny patří do kterých kategorií
# v rámci snídaně a jejich procentuelní zastoupení
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
	"SELECT z.id, z.baleni, p.nazev, p.kj, mj.zkratka, z.baleni * p.kj FROM zasoby z JOIN potraviny p on z.id_potraviny = p.id JOIN merna_jednotka mj on p.id_merna_jednotka = mj.id")
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


kategrie_snidane = {
	"slane_pecivo":[56, 57],
	"sladke_pecivo":[58],
	"jogurty":[26, 27],
	"ovoce":[53],
	"zelenina":[55],
	"prilohy_pro_slane_pecivo":[63, 62, 52, 37, 36, 35, 34, 33, 32, 31, 
		28, 27, 26, 22, 21, 20, 18, 17, 16, 14, 12],
	"prilohy_pro_sladke_pecivo":[67, 66, 65, 64, 54, 52, 48, 27, 26],
	"prilohy_pro_jogurty":[28, 35, 39, 48, 52, 54, 61, 64, 65, 66, 67],
	"napoje":[30, 41, 42, 44, 45, 46]
}

#kategorie1 = slane_pecivo, sladke_pecivo a jogurty
#kategorie2 = ovoce, zelenina
#kategorie3 = prilohy pro slane pecivo, prilohy pro sladke pecivo a prilohy pro jogurty
#kategorie4 = napoje

def vyber_zakladni_kosik_snidane ():
	zakladni_kosik = ["sladke_pecivo", "slane_pecivo", "jogurty"]
	return random.choice(zakladni_kosik)

kj_potrebne_snidane_K1 = kj_potrebne_snidane*0.5
#kj_potrebne_snidane_K1 = 20000

print("KJ potrebne ke snidani: {}".format(kj_potrebne_snidane))
print("KJ potrebne ke snidani K1: {}".format(kj_potrebne_snidane_K1))


def velky_select():
	'''
	tento select tam davam, protoze na zacatku sestavovani celeho jidelnicku 
	musime mit vsechny hodnoty v Pythonu, abychom pozdeji, az sestavime jidelnicek, 
	mohli upravit databazi (tzn. odebrat a nebo zmenit mnozstvi potraviny)
	!!!! U velkeho selectu si musime detailne hlidat, na ktere pozici co je!!!
	'''
	return select_all("""SELECT 
		p.nazev, z.baleni, p.kj, mj.zkratka, z.baleni * p.kj, p.id_kategorie
		FROM zasoby z 
		JOIN potraviny p on z.id_potraviny = p.id 
		JOIN merna_jednotka mj on p.id_merna_jednotka = mj.id""")

def vyber_jidla_z_kategorii(IDs):
	'''tato funkce vrati nazvy potravin odpovidajici ID kategorií'''
	nazvy_jidel = []
	for i in TABULKA_ZASOB:
		if i[5] in IDs:
			nazvy_jidel.append(i) #pokud bude potravina v kategorii potrebnych ID, prida ji do seznamu
	return nazvy_jidel


def vyber_jidla_s_nejvice_KJ(seznam_jidel):
	return max(seznam_jidel, key=lambda x:x[4]) #fce, ktera vrati potravinu s nejvyssi postej KJ


def logika_vypoctu(kategorie_ID):
	vybrane_jidlo = None
	vybrane_jidlo_2 = None
	KJ_k_prevedeni = None
	pouzita_gramaz = None
	pouzita_gramaz_2 = None

	jidla_z_kategorii = vyber_jidla_z_kategorii(kategorie_ID)
	vybrane_jidlo = vyber_jidla_s_nejvice_KJ(jidla_z_kategorii)
	
	if vybrane_jidlo[4] >= kj_potrebne_snidane_K1:
		pouzita_gramaz = int(vybrane_jidlo[1]*kj_potrebne_snidane_K1)/float(vybrane_jidlo[4])
		#print(pouzita_gramaz)
		zbyla_gramaz = vybrane_jidlo[1]-pouzita_gramaz
		#print(zbyla_gramaz)
		TABULKA_ZASOB.remove(vybrane_jidlo)
		TABULKA_ZASOB.append((vybrane_jidlo[0], zbyla_gramaz, vybrane_jidlo[2], vybrane_jidlo[3], zbyla_gramaz*float(vybrane_jidlo[2]), vybrane_jidlo[5]))
		'''
		Tady jsem z tabulky musela smazat vybrane jidlo, ktere jsem pouzila, 
		ale pokud ta gramaz byla vetsi nez pozadovana, tak jsem si do tabulky
		nazpet hodila novy zaznam, kde je ponizena gramaz a KJ. Protoze je v 
		seznamu.append vice kriterii, musela jsem tam pouzit dve zavorky - 
		ty mi rikaji, ze jsem pridala jeden tuple do seznamu.
		'''
	else:
		#ted mame nedostatek KJ, tak chceme vybrat jidlo s nejvice KJ jeste jednou a pouzit ho do naseho vyberu
		TABULKA_ZASOB.remove(vybrane_jidlo)
		jidla_z_kategorii_2 = vyber_jidla_z_kategorii(kategorie_ID) #protoze se fce odvolava na vyber jidla z kategorii, museli jsme udelat i 2, protoze jinak se dane jidlo s nejvyssimi KJ smazalo z TABULKY_ZASOB, tak je potreba ji znovu nacist( uz bez te smazane potraviny)
		vybrane_jidlo_2 = vyber_jidla_s_nejvice_KJ(jidla_z_kategorii_2)
		#print(vybrane_jidlo_2)
		 #timto jsem odebrala tu prvni potravinu, ktera nedostacuje KJ

		if vybrane_jidlo_2[4] >= kj_potrebne_snidane_K1-vybrane_jidlo[4]:
			pouzita_gramaz_2 = int(vybrane_jidlo_2[1]*(kj_potrebne_snidane_K1-vybrane_jidlo[4]))/float(vybrane_jidlo_2[4])
			zbyla_gramaz_2 = vybrane_jidlo_2[1]-pouzita_gramaz_2
			#print(vybrane_jidlo_2)
			TABULKA_ZASOB.remove(vybrane_jidlo_2)
			TABULKA_ZASOB.append((vybrane_jidlo_2[0], zbyla_gramaz_2, vybrane_jidlo_2[2], vybrane_jidlo_2[3], zbyla_gramaz_2*float(vybrane_jidlo_2[2]), vybrane_jidlo_2[5]))
		else:
			TABULKA_ZASOB.remove(vybrane_jidlo_2)
			pouzita_gramaz_2 = int(vybrane_jidlo_2[1]*(kj_potrebne_snidane_K1-vybrane_jidlo[4]))/float(vybrane_jidlo_2[4])
			zbyla_gramaz_2 = vybrane_jidlo_2[1]-pouzita_gramaz_2
			KJ_k_prevedeni = kj_potrebne_snidane_K1-vybrane_jidlo[4]-vybrane_jidlo_2[4]

	#print(vybrane_jidlo)
	#print(vybrane_jidlo_2)
	#print(zbyla_gramaz_2)
	#print(pouzita_gramaz_2)
	#print(KJ_k_prevedeni)
	return (vybrane_jidlo, vybrane_jidlo_2, KJ_k_prevedeni, pouzita_gramaz, pouzita_gramaz_2)	

TABULKA_ZASOB = velky_select()
print(logika_vypoctu(kategrie_snidane["slane_pecivo"]))
