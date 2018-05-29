import psycopg2
import random

def selecty_z_databaze(select):
	conn = psycopg2.connect(dbname="****", user="****", password= "****", host="da.stderr.cz") #ted se zacnu pripojovat do dataaze
	cur1 = conn.cursor() #pomoci cursoru delam to, co chci delat na databazi

	cur1.execute(select) 
	return cur1.fetchall() 

tabulka_potravin = selecty_z_databaze("SELECT p.nazev, p.kj, mj.nazev FROM potraviny p join merna_jednotka mj on p.id_merna_jednotka = mj.id")



kj_potrebne = 40

kj_potrebne_snidane = int(kj_potrebne/100*20)
kj_potrebne_svacina1 = int(kj_potrebne/100*10)
kj_potrebne_obed = int(kj_potrebne/100*35)
kj_potrebne_svacina2 = int(kj_potrebne/100*10)
kj_potrebne_vecere = int(kj_potrebne/100*25)


def vyber_jidla(KJ_k_snedku):
	vybrane_kj = 0
	seznam_vybranych_potravin=[]
	tabulka_potravin_pro_funkci = list(tabulka_potravin) #slovo list je zde pridane, protoze bez toho nam to stale chtelo tahat data z prazdne tabulky
	
	while (vybrane_kj < KJ_k_snedku and len(tabulka_potravin_pro_funkci)!=0):
		vybrana_potravina = random.choice(tabulka_potravin_pro_funkci)
		tabulka_potravin_pro_funkci.remove(vybrana_potravina)
		vybrana_potravina_nazev = vybrana_potravina[0]
		vybrana_potravina_kj = vybrana_potravina[1]
		#print(tabulka_potravin)

		if vybrana_potravina_kj < KJ_k_snedku - vybrane_kj:
			seznam_vybranych_potravin.append(vybrana_potravina)
			vybrane_kj = vybrane_kj + vybrana_potravina_kj
			print(vybrane_kj)
		else:
			continue

	return (vybrane_kj, seznam_vybranych_potravin)



SNIDANE = vyber_jidla(kj_potrebne_snidane)
print(SNIDANE)

SVACINA1 = vyber_jidla(kj_potrebne_svacina1)
print(SVACINA1)

OBED = vyber_jidla(kj_potrebne_obed)
print (OBED)

SVACINA2 = vyber_jidla(kj_potrebne_svacina2)
print(SVACINA2)

VECERE = vyber_jidla(kj_potrebne_vecere)
print(VECERE)
