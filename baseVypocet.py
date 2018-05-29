#TENTO FILE OBSAHUJE POUZE TESTOVACI, NATVRDO NASAZENE HODNOTY JIDELNICKU

from polozka_jidelnicku import Polozka_jidelnicku

class BaseVypocet():

	def get_snidane():
	  return [Polozka_jidelnicku("broskve", 150, "g"),
	  Polozka_jidelnicku("jogurt", "200 g")]

	def get_svacina_dopo():
	  return [Polozka_jidelnicku("ananas", "150 g")]

	def get_obed():
	  return [Polozka_jidelnicku("testoviny", "150 g"),
	  Polozka_jidelnicku("kureci maso", "150 g")]

	def get_svacina_odpo():
	  return [Polozka_jidelnicku("cottage", "250 g")]

	def get_vecere():
	  return [Polozka_jidelnicku("tortila", "60 g"),
	  Polozka_jidelnicku("fazole", "100 g")]


