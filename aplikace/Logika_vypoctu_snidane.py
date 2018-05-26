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

kj_potrebne_snidane = int(denni_prijem_kj/100*20)
#kj_potrebne_snidane = 100000															# doporucene rozlozeni chodu: snidane 20-25%
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


kategorie_snidane = {
	"slane_pecivo":[56, 57],
	"sladke_pecivo":[58],
	"jogurty":[26, 27],
	"cerealie_vlocky": [70],
	"ovoce":[53],
	"zelenina":[55],
	"prilohy_pro_slane_pecivo":[63, 62, 52, 37, 35, 34, 33, 32, 31, 
		28, 27, 26, 22, 21, 20, 18, 17, 16, 14, 12],
	"prilohy_pro_sladke_pecivo":[67, 66, 64, 54, 52, 48, 27, 26],
	"prilohy_pro_cerealie" :[67, 66, 65, 54, 52, 48, 27, 26],
	"prilohy_pro_jogurty":[28, 35, 39, 48, 52, 54, 61, 64, 65, 66, 67],
	"napoje":[30, 41, 42, 44, 45, 46]
}

# kosik1 = slane_pecivo, sladke_pecivo a jogurty 50%
# kosik2 = ovoce, zelenina 20%
# kosik3 = prilohy pro slane pecivo, prilohy pro sladke pecivo a prilohy pro jogurty 25%
# kosik4 = napoje 5%

def vyber_zakladni_kosik (zakladni_kosik):
	return random.choice(zakladni_kosik)

kj_potrebne_snidane_K1 = kj_potrebne_snidane*0.5
#kj_potrebne_snidane_K1 = 2000000


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


def logika_vypoctu(kategorie_ID, KJ, max_pocet_potravin=None):
	#max_pocet_potravin - je ten, ktery si definuju u jednotlivych kosicku (např. u K1 chci max dve ruzne potraviny, ale jako vychozi hodnota fce je nekonecno)
	vybrane_jidlo = None
	KJ_k_prevedeni = None
	pouzita_gramaz = None
	spotrebovane_KJ = 0
	pocet_potravin = 0
	jidelnicek = []
	KJ_k_prevedeni = 0

	jidla_z_kategorii = vyber_jidla_z_kategorii(kategorie_ID)
	
	if max_pocet_potravin is None:
		max_pocet_potravin = len(jidla_z_kategorii)
	# tento if tady mam, protoze u nekterych kosicku (napr. ovoce nebo zelenina)
	# je mi jedno, jestli mi to vybere 20 druhu ovoce nebo zeleniny
	# kdyby to nebylo definovane, muze to hazet chybu, protoze ta tabulka je
	# strasne kratka a pritom jsme nezaplnili potrebne KJ, takze ono by se to 
	# snazilo porad pokracovat dal a nezastavilo by se to. 
	
	while KJ >= spotrebovane_KJ and pocet_potravin < max_pocet_potravin:
		vybrane_jidlo = vyber_jidla_s_nejvice_KJ(jidla_z_kategorii)
		pocet_potravin += 1
		jidlo = {
			"nazev" : vybrane_jidlo[0],
			"baleni" : vybrane_jidlo[1],
			"KJ_na_gram_kus" : vybrane_jidlo[2],
			"jednotka" : vybrane_jidlo[3],
			"vysledne_KJ" : vybrane_jidlo[4]
		}

		if jidlo["vysledne_KJ"] >= KJ - float(spotrebovane_KJ):
			# tady řešíme možnost, že vybrané jídlo má hned na první pokus více KJ než potřebných
			pouzita_gramaz = int(int(jidlo["baleni"]*KJ)/float(jidlo["vysledne_KJ"]))
			#print(pouzita_gramaz)
			zbyla_gramaz = jidlo["baleni"]-pouzita_gramaz
			#print(zbyla_gramaz)
			TABULKA_ZASOB.remove(vybrane_jidlo)
			TABULKA_ZASOB.append((jidlo["nazev"], zbyla_gramaz, jidlo["KJ_na_gram_kus"], jidlo["jednotka"], zbyla_gramaz*float(vybrane_jidlo[2]), vybrane_jidlo[5]))
			jidelnicek.append((jidlo["nazev"], pouzita_gramaz, jidlo["jednotka"], pouzita_gramaz * int(jidlo["KJ_na_gram_kus"])))
			break	
		
		# Tady jsem z tabulky musela smazat vybrane jidlo, ktere jsem pouzila, 
		# ale pokud ta gramaz byla vetsi nez pozadovana, tak jsem si do tabulky
		# nazpet hodila novy zaznam, kde je ponizena gramaz a KJ. Protoze je v 
		# seznamu.append vice kriterii, musela jsem tam pouzit dve zavorky - 
		# ty mi rikaji, ze jsem pridala jeden tuple do seznamu.
		
		else:
			#ted mame nedostatek KJ, tak chceme vybrat jidlo s nejvice KJ a pouzit ho do naseho vyberu
			spotrebovane_KJ = jidlo["vysledne_KJ"] + spotrebovane_KJ
			#print(vybrane_jidlo)
			TABULKA_ZASOB.remove(vybrane_jidlo)
			jidla_z_kategorii.remove(vybrane_jidlo)
			jidelnicek.append((jidlo["nazev"], jidlo["baleni"], jidlo["jednotka"], jidlo["vysledne_KJ"]))
			KJ_k_prevedeni = KJ_k_prevedeni + (KJ - float(spotrebovane_KJ))
					

	#print(vybrane_jidlo)
	#print(vybrane_jidlo_2)
	#print(zbyla_gramaz_2)
	#print(pouzita_gramaz_2)
	#print(KJ_k_prevedeni)
	return (KJ_k_prevedeni, jidelnicek)

TABULKA_ZASOB = velky_select()
#print(logika_vypoctu(kategorie_snidane["slane_pecivo"], 700))

print("KJ potrebne ke snidani: {}".format(kj_potrebne_snidane))
#print("KJ potrebne ke snidani K1: {}".format(kj_potrebne_snidane_K1))

def vytvor_snidani():
	zakladni_kosik = vyber_zakladni_kosik (["sladke_pecivo", "slane_pecivo", "jogurty", "cerealie_vlocky"])
	kosik_2 = "ovoce"
	if zakladni_kosik is "slane_pecivo":
		kosik_2 = "zelenina"
		kosik_3 = "prilohy_pro_slane_pecivo"
	elif zakladni_kosik is "sladke_pecivo":
		kosik_3 = "prilohy_pro_sladke_pecivo"
	elif zakladni_kosik is "cerealie_vlocky":
		kosik_3 = "prilohy_pro_cerealie"
	else:
		kosik_3 = "prilohy_pro_jogurty"

	snidane_K1 = logika_vypoctu(kategorie_snidane[zakladni_kosik], kj_potrebne_snidane*0.5, 2)
	print(snidane_K1)
	snidane_K2 = logika_vypoctu(kategorie_snidane[kosik_2], kj_potrebne_snidane*0.2)
	print(snidane_K2)
	snidane_K3 = logika_vypoctu(kategorie_snidane[kosik_3], kj_potrebne_snidane*0.25)
	print(snidane_K3)
	snidane_K4 = logika_vypoctu(kategorie_snidane["napoje"], kj_potrebne_snidane*0.05)
	print(snidane_K4)
vytvor_snidani()






kategorie_obed = {
	"maso_rostlinne_alternativy_syra":[13, 15, 23, 25, 62],
	"prilohy_k_masu_nebo_rostl_alt_syra":[10, 78, 81, 79],
	"ryby":[19],
	"prilohy_k_rybam" :[10, 79],
	"hotove_jidlo_hodi_se_knedliky": [80],
	"prilohy_k_hotove_jidlo_hodi_se_knedliky":[77],
	"hotove_jidlo_hodi_se_knedliky_nebo_testoviny":[82],
	"prilohy_k_hotove_jidlo_hodi_se_knedliky_nebo_testoviny":[77, 78],
	"hotove_jidlo_potreba_priloha":[3, 4],
	"prilohy_hotove_jidlo_potreba_priloha" :[10],
	"hotove_jidlo_netreba_priloha":[72, 73],
	"hotove_jidlo_sladke" : [71],
	"lusteniny" :[50],
	"prilohy_k_lusteninam": [14, 16, 22],
	"mc_donald":[5],
	"pizza":[6],
	"piti" : [41, 42, 43, 44, 45, 46],
	"salaty" : [51, 55, 69],
	"prilohy_k_salatum" : [13, 15, 62, 19, 24, 25, 18, 22, 31, 32, 34],
	"testoviny" : [78, 85],
	"prilohy_k_testovinam" : [13, 15, 62, 19, 23, 24, 25, 47, 18, 19, 22, 31, 32, 34],
	"ovoce" : [53]
}

print("KJ potrebne ke obedu: {}".format(kj_potrebne_obed))


def vytvor_obed ():
	seznam_hlavnich_jidel = ["maso_rostlinne_alternativy_syra","ryby", 
	"hotove_jidlo_hodi_se_knedliky", "hotove_jidlo_hodi_se_knedliky_nebo_testoviny",
	"hotove_jidlo_potreba_priloha", "hotove_jidlo_netreba_priloha",
	"hotove_jidlo_sladke", "lusteniny", "mc_donald", "pizza", "salaty", "testoviny"]
	zakladni_kosik = vyber_zakladni_kosik (seznam_hlavnich_jidel)
	if zakladni_kosik is "maso_rostlinne_alternativy_syra":
		priloha = "prilohy_k_masu_nebo_rostl_alt_syra"
	elif zakladni_kosik is "ryby":
		priloha = "prilohy_k_rybam"
	elif zakladni_kosik is "hotove_jidlo_hodi_se_knedliky":
		priloha = "prilohy_k_hotove_jidlo_hodi_se_knedliky"
	elif zakladni_kosik is "hotove_jidlo_hodi_se_knedliky_nebo_testoviny":
		priloha = "prilohy_k_hotove_jidlo_hodi_se_knedliky_nebo_testoviny"
	elif zakladni_kosik is "hotove_jidlo_potreba_priloha":
		priloha = "prilohy_hotove_jidlo_potreba_priloha"
	elif zakladni_kosik is "hotove_jidlo_netreba_priloha":
		priloha = None
	elif zakladni_kosik is "hotove_jidlo_sladke":
		priloha = None
	elif zakladni_kosik is "lusteniny":
		priloha = "prilohy_k_lusteninam"
	elif zakladni_kosik is "mc_donald":
		priloha = None
	elif zakladni_kosik is "pizza":
		priloha = None
	elif zakladni_kosik is "salaty":
		priloha = "prilohy_k_salatum"
	elif zakladni_kosik is "testoviny":
		priloha = "prilohy_k_testovinam"

	

	if priloha is not None:
		KJ = 0.5
	else:
		KJ = 0.8
	obed_K1 = logika_vypoctu(kategorie_obed[zakladni_kosik], kj_potrebne_obed*KJ)
	print(obed_K1)

	obed_K2 = []
	if priloha is not None:
		obed_K2 = logika_vypoctu(kategorie_obed[priloha], kj_potrebne_obed*0.3)
	print(obed_K2)

	
	if zakladni_kosik is not "hotove_jidlo_sladke":
		zelenina_ovoce = "salaty"
	else:
		zelenina_ovoce = "ovoce"

	obed_K3 = []
	if zakladni_kosik is not "salaty":
		obed_K3 = logika_vypoctu(kategorie_obed[zelenina_ovoce], kj_potrebne_obed*0.2)
	print(obed_K3)



vytvor_obed()







#kdyz to vybere kategorii, kde nic nemam v zasobach, musi to vybrat jinou kategorii!!!!
# opravit salaty!!!!
# krati to porce u veci, co jsou na kus (chce to vzit napr 0,8 ks, coz se zaokrouhlenim 
#vypise jako nula a pak se i kalorie nasobi nulou,takze vychazi nula )