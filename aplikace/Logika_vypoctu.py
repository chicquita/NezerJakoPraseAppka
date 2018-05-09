import psycopg2
import random

def selecty_z_databaze(select):
	conn = psycopg2.connect(dbname="****", user="****", password= "****", host="da.stderr.cz") #ted se zacnu pripojovat do dataaze
	cur1 = conn.cursor() #pomoci cursoru delam to, co chci delat na databazi

	cur1.execute(select) 
	return cur1.fetchall() 

tabulka_potravin = selecty_z_databaze("SELECT p.nazev, p.kj, mj.nazev FROM potraviny p join merna_jednotka mj on p.id_merna_jednotka = mj.id")


kj_potrebne = 30
vybrane_kj = 0
seznam_vybranych_potravin=[]
while (vybrane_kj < kj_potrebne and len(tabulka_potravin)!=0):
	vybrana_potravina = random.choice(tabulka_potravin)
	tabulka_potravin.remove(vybrana_potravina)
	vybrana_potravina_nazev = vybrana_potravina[0]
	vybrana_potravina_kj = vybrana_potravina[1]
	#print(tabulka_potravin)

	if vybrana_potravina_kj < kj_potrebne - vybrane_kj:
		seznam_vybranych_potravin.append(vybrana_potravina)
		vybrane_kj = vybrane_kj + vybrana_potravina_kj
		print(vybrane_kj)
	else:
		continue

print(seznam_vybranych_potravin)
print(vybrane_kj)




#skoncime, kdyz kj_potrebne - suma i je rovno 0 nebo kdyz kj_potrebne - suma i < nez min i



	#koukni do seznamu a vyber potravinu s jejich kj.
	#kj vybrane potraviny vem a odecti je od kj_potrebnych
	#pokud je i < kj_potrebne vyber potravinu s jejich kj
	#.
	#.
	#kdyz je i > nez kj_potrebne, neber je v potaz

	#kdyz je i nula, vypis seznam potravinu

	#kdyz od kj_potrebnych nejde odecist i, protoze je kj_potrebnych uz malo, 
	#vypis seznam potravin a napis, ze chybi zbyly pocet kj.
	#haze to chybu, protoze jsme skoncili na sume 29, 
	#proto musime do kodu nejak zaclenit, ze se jednotlivy hodnoty, ktery program
	#videl, napisou do seznamu a program bude koukat jenom na zyble potraviny. Dokud zbyly seznam nebude prazdny

