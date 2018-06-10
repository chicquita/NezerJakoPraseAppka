import psycopg2
import sys
"""
Skript pro generovani nahodnych dat do zasobovaci tabulky.

na zacatku jsou dve promenne:
* TABULKA: nazev tabulky, ktera se ma prepisovat
           (nedoporucuju pracovat primo s tabulkou "zasoby", pac nevim, jak se to bude chovat :))
* POCET_ZASOB: kolik jidel tam ma byt.

Mnozstvi se bere random z tohoto rozmezi:
gramy: 100 - 500
pro ml: 100 - 1000 ml
pro ks: 1 - 10 ks
pro porce: 1 - 5
"""

TABULKA= "test_zasoby_1"
POCET_ZASOB = 20

try:
    conn = psycopg2.connect(dbname="janicka", user="janicka", password= "Tajne heslo, ktere neni na githubu", host="da.stderr.cz")
    cur = conn.cursor()
except:
    sys.exit("Nedokazu se pripojit k databazi, koncim")

q_mazani = "DROP TABLE IF EXISTS {}".format(TABULKA)
q_tabulka ="""CREATE TABLE {} (
    id serial primary key
    ,id_potraviny int references potraviny (id)
    ,baleni int
    ,id_domacnost int references domacnost (id)
    )""".format(TABULKA)
q_generator = """
with p as (
  select
    p.id as id
    ,p.nazev as nazev
    ,mj.zkratka as zkratka
  from potraviny p
  join merna_jednotka mj on mj.id = p.id_merna_jednotka
  order by random()
  limit {}
) insert into {} ( id_potraviny, baleni, id_domacnost ) select
  id
  ,CASE WHEN zkratka='g' THEN floor(random() * (500-100+1) + 100)::int -- 100 - 500g
         WHEN zkratka='ml' THEN floor(random() * (1000-100+1) + 100)::int -- 100 - 1000 ml
         when zkratka='ks' THEN floor(random() * (10-1+1) + 1)::int -- 1 - 10ks
         when zkratka='pc' THEN floor(random() * (5-1+1) + 1)::int -- 1 - 5 porci
         ELSE 0 -- fuck it
    END
  ,1
from p""".format(POCET_ZASOB,TABULKA)


try:
    cur.execute(q_mazani)
    cur.execute(q_tabulka)
    cur.execute(q_generator)
    conn.commit()
    print("{} nahodnych potravin je v tabulce '{}'".format(POCET_ZASOB, TABULKA))
except:
    conn.rollback()
    print("Jejda, neco se nepovedlo")
