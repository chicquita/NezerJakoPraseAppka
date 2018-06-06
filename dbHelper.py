#OBSAHUJE PRIPOJENI DO DB A ZAKLADNI SELECTY

import psycopg2

class DbHelper():
	

	def __init__(self, dbname, user, password):
		self.connection = psycopg2.connect(dbname=dbname, 
			user=user, 
			password= password, 
			host="da.stderr.cz")
		self.connection.autocommit = True
		self.cursor = self.connection.cursor()


	#vraci matici
	def select_all(self, select, binds = None):				
		if binds:
			self.cursor.execute(select, binds)
		else:
			self.cursor.execute(select)			
		return self.cursor.fetchall() 		

	#vraci 1 radek
	def select_single_row(self, select, binds = None):
		result_set = self.select_all(select, binds)
		if not result_set:
			raise Exception ("chces vytahnout 1 hodnotu z DB ale nevrartilo to ani 1 radek")

		return result_set[0] 


	#vraci 1 hodnotu
	def select_single_value(self, select, binds = None):
		single_row = self.select_single_row( select, binds)
	
		return single_row[0]   


	def insert(self, insert, binds = None):
		self.cursor.execute(insert, binds)


