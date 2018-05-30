#TENTO FILE OBSAHUJE POUZE TESTOVACI, NATVRDO NASAZENE HODNOTY JIDELNICKU

from polozka_jidelnicku import Polozka_jidelnicku
from dbHelper import DbHelper
import funkce

class BaseVypocet():

	def __init__(self):
		funkce.nacti_zasoby()
		self.db = DbHelper("janicka", "janicka", "Tajne heslo, ktere neni na githubu")
		self.denni_prijem_kj = self.db.select_single_value("SELECT u.denni_prijem_kj FROM uzivatel u WHERE id = 1")
		self.kj_potrebne_snidane = int(self.denni_prijem_kj/100*20)			 # snidane 20%
		self.kj_potrebne_svacina = int(self.denni_prijem_kj/100*10)          # svacina 10-15%
		self.kj_potrebne_obed = int(self.denni_prijem_kj/100*35)              # obed 30-35%
		self.kj_potrebne_vecere = int(self.denni_prijem_kj/100*25)            # vecere 15-25%

		self.prebytek_ze_snidane = 0
		self.prebytek_z_obeda = 0

	def _formatuj_vystup(self,jidla):
		vypis = []
		for jidlo in jidla:
			nazev = jidlo[0]
			mnozstvi = "{} {}".format(jidlo[1], jidlo[2])

			vypis.append(Polozka_jidelnicku(nazev, mnozstvi))

		return vypis


	def get_snidane(self):
		snidane = funkce.vytvor_snidani(self.kj_potrebne_snidane)
		self.prebytek_ze_snidane = snidane[0]
		return self._formatuj_vystup(snidane[1])

	def get_svacina_dopo(self):
		svacina = funkce.vytvor_svacinu(self.kj_potrebne_svacina)
		return self._formatuj_vystup(svacina[1])

	def get_obed(self):
		obed = funkce.vytvor_obed(self.kj_potrebne_obed + self.prebytek_ze_snidane)
		self.prebytek_z_obeda = obed[0]
		return self._formatuj_vystup(obed[1])

	def get_svacina_odpo(self):
		svacina = funkce.vytvor_svacinu(self.kj_potrebne_svacina)
		return self._formatuj_vystup(svacina[1])

	def get_vecere(self):
		vecere = funkce.vytvor_veceri(self.kj_potrebne_vecere + self.prebytek_z_obeda)
		return self._formatuj_vystup(vecere[1])


