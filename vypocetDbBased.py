''' TO DO:
DOPLNIT REZERVACI POTRAVIN V DB
FUNKCE DO BALIKU
CLASSY DO SEPARATE FILU
PODMINKA EXISTUJI NADEFINOVANE SETY
'''


import random
from polozka_jidelnicku import Polozka_jidelnicku
from dbHelper import DbHelper
from baseVypocet import BaseVypocet


class VypocetDbBased(BaseVypocet):

	SNIDANE_ID = 1
	SVACINA_DOPO_ID = 2
	OBED_ID = 3
	SVACINA_ODPO_ID = 4
	VECERE_ID = 5

	def __init__(self):
		self.db = DbHelper("ada", "ada", "To heslo ti nereknu")

	def get_snidane(self):
		return self.get_dennichod(self.SNIDANE_ID)

	def get_svacina_dopo(self):
		return get_dennichod(self.SVACINA_DOPO_ID) 

	def get_obed(self):
		return get_dennichod(self.OBED_ID) 

	def get_svacina_odpo(self):
		return get_dennichod(self.SVACINA_ODPO_ID) 

	def get_vecere(self):
		return get_dennichod(self.VECERE_ID)


	def get_dennichod(self, dennichod_id):

		denni_prijem_kj = self.db.select_single_value("SELECT u.denni_prijem_kj FROM uzivatel u WHERE id = 1")


		mozne_patterny = self.db.select_all("SELECT p.id FROM Pattern p JOIN denni_chody dch ON p.id_denni_chody = dch.id WHERE 0 < all(SELECT sum(CASE WHEN (z.mnozstvi-z.blokovano)*pom.kj >= dch.zastoupeni_procenta * pl.ratio * %s then 1 else 0 END) FROM pattern_line pl JOIN pattern_line_set pls ON pl.id_pattern = pls.id_pattern and pl.line = pls.pattern_line JOIN potraviny_kat_skup pom ON pls.id_potraviny = pom.id_potravina or pls.id_kategorie = pom.id_kategorie or pls.id_skupina = pom.id_skupina LEFT JOIN zasoby z ON pom.id_potravina = z.id_potraviny WHERE pl.id_pattern = p.id GROUP BY pl.id_pattern, pl.line) and exists(select 1 from pattern_line pl where pl.id_pattern = p.id) and p.id_denni_chody = %s", (denni_prijem_kj, dennichod_id,)) 

		if not mozne_patterny:
			raise Exception ("nenalezen ani jeden vhodny pattern")

		vybrany_pattern = random.choice(mozne_patterny)[0]
		print(vybrany_pattern)

		mozne_potraviny = self.db.select_all("SELECT pl.line, pom.id_potravina, pot.nazev, round(dch.zastoupeni_procenta * pl.ratio * %s/pot.kj) as mnozstvi, mj.zkratka FROM pattern_line pl JOIN Pattern p on pl.id_pattern = p.id JOIN denni_chody dch ON p.id_denni_chody = dch.id JOIN pattern_line_set pls ON pl.id_pattern = pls.id_pattern and pl.line = pls.pattern_line JOIN potraviny_kat_skup pom ON pls.id_potraviny = pom.id_potravina or pls.id_kategorie = pom.id_kategorie or pls.id_skupina = pom.id_skupina JOIN zasoby z ON pom.id_potravina = z.id_potraviny JOIN potraviny pot on pot.id = pom.id_potravina JOIN merna_jednotka mj on pot.id_merna_jednotka = mj.id WHERE (z.mnozstvi-z.blokovano)*pom.kj >= dch.zastoupeni_procenta * pl.ratio * "+ str(denni_prijem_kj)+" and p.id = %s", (denni_prijem_kj, vybrany_pattern,))

		pocet_lines = self.db.select_single_value("select COUNT (*) from pattern_line pl where pl.id_pattern = %s", (vybrany_pattern,))
		

		polozky_jidelnicku = []
		for i in range(1, pocet_lines+1):
	  		vybrana_polozka = random.choice(list(filter(lambda x: x[0] == i, mozne_potraviny)))
	  		polozky_jidelnicku.append(Polozka_jidelnicku(vybrana_polozka[2],str(vybrana_polozka[3]) +" "+ vybrana_polozka[4]))

		print(polozky_jidelnicku)


		return polozky_jidelnicku

		
