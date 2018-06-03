# toto je soubor, ktery bych v budoucnu chtela naimplementovat primo do 
# databaze, ale z casovych duvodu je to prozatim tady.
TABULKA_ZASOB = []


snidane = {
	"slane_pecivo":[56, 57],
	"sladke_pecivo":[58],
	"jogurty":[26, 27],
	"cerealie_vlocky": [70],
	"ovoce":[53],
	"zelenina":[55, 86],
	"prilohy_pro_slane_pecivo":[63, 62, 52, 37, 35, 34, 33, 32, 31, 
		28, 27, 26, 22, 21, 20, 18, 17, 16, 14, 12],
	"prilohy_pro_sladke_pecivo":[66, 64, 54, 52, 48, 27, 26],
	"prilohy_pro_cerealie" :[66, 54, 52, 48, 27, 26],
	"prilohy_pro_jogurty":[28, 35, 39, 48, 52, 54, 61, 64, 66],
	"napoje":[30, 41, 42, 44, 45, 46]
}

# kosik1 = slane_pecivo, sladke_pecivo a jogurty 50%
# kosik2 = ovoce, zelenina 20%
# kosik3 = prilohy pro slane pecivo, prilohy pro sladke pecivo a prilohy pro jogurty 25%
# kosik4 = napoje 5%


obed = {
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
	"salaty" : [86],
	"prilohy_k_salatum" : [13, 15, 62, 19, 25, 18, 22, 31, 32, 34],
	"testoviny" : [78, 85],
	"prilohy_k_testovinam" : [13, 15, 62, 19, 23, 25, 47, 18, 19, 22, 31, 32, 34],
	"ovoce" : [53],
	"zelenina" : [55, 69],
	"spagety": [85],
	"prilohy_ke_spagetam": [13, 15, 62, 19, 23, 25, 47, 18, 19, 22, 31, 32, 34]
}


vecere = {
	"maso_rostlinne_alternativy_syra" :[13, 15, 23, 25, 62],
	"prilohy_k_masu_nebo_rostl_alt_syra":[10, 78, 81, 79, 56, 57, 79],
	"ryby":[19],
	"prilohy_k_rybam" :[10, 79],
	"lusteniny" :[50],
	"prilohy_k_lusteninam": [14, 16, 22],
	"pecivo": [56, 57, 79, 83],
	"prilohy_k_pecivu": [14, 16, 17, 12, 18, 20, 31, 32, 33, 34, 76, 21, 22],
	"uzeniny": [14, 16],
	"prilohy_k_uzeninam": [56],
	"polevky": [7, 8, 9],
	"prilohy_k_polevkam" : [56],
	"salaty": [86],
	"prilohy_k_salatum": [13, 15, 62, 19, 25, 18, 22, 31, 32, 34],
	"jogurty_a_mlecne_vyrobky": [26, 27, 35, 28],
	"prilohy_k_jogurtum_a_mlecnym vyrobkum": [52, 53, 70],
	"tlacenky": [76],
	"prilohy_k_tlacenkam": [56],
	"testoviny" : [78, 85],
	"prilohy_k_testovinam" : [13, 15, 62, 19, 23, 25, 47, 18, 19, 22, 31, 32, 34],
	"chlebicky": [87],
	"pizza":[6],
	"mc_donald": [5],
	"zelenina": [55],
	"ovoce": [53]
}


svacina = {
	"krehky_chleb_knackebrot" : [57],
	"prilohy_pro_krehky_chleb_knackebrot" : [18, 31, 32, 33, 34],
	"jogurty_a_mlecne_vyrobky" : [26, 27, 35],
	"prilohy_pro_jogurty_a_mlecne_vyrobky" : [52, 53, 54],
	"kysane_mlecne_napoje" : [28],
	"prilohy_pro_kysane_mlecne_napoje" : [52, 53, 54],
	"ovoce" : [53],
	"prilohy_pro_ovoce" : [64, 52],
	"sladkosti" : [64, 65, 66, 54],
	"prilohy_pro_sladkosti" : [53]
}
