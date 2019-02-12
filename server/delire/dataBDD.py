import pandas
import math
import numpy as np
from collections import OrderedDict as dic

from .models import Noeud, Personne, Specialite, Document, Ecrit, EmpSpe, NoeudSpe

EXCEL_FILE = "delire/data.xlsx"

SHEETS = dic([ ("PersonneClient", Personne), ("Noeud", Noeud), ("PersonneAPHP", Personne),
		   ("Spécialité", Specialite), ("Document", Document), ("Ecrit", Ecrit),
		   ("EmpSpe", EmpSpe), ("NoeudSpe", NoeudSpe) ])

def getDF(file, sheet):
	return pandas.read_excel(file, sheet_name=sheet)
	
def treatRow(row, labels, table, vars):
	kwargs = {}
	for y in labels:
		data = row.loc[row.index[0], y]
		
		if type(data) == float or type(data) == np.float64:

			if math.isnan(data):
				continue
				
		if data in vars:  # Variables en maj dans tableau
			data = vars[data]
		
		kwargs[y] = data
	
	if "var" not in kwargs:
		raise ValueError("Besoin de remplir la colonne var dans chaque feuille de l'excel")
	
	var = kwargs.pop("var")
	
	for k, v in kwargs.items():
		if v in vars:
			kwargs[k] = vars[v]
	
	return (var, table.objects.create(**kwargs))

def createData():
	dfs = {x : getDF(EXCEL_FILE, x) for x in SHEETS}
	
	
	vars = {}
	for sheet in SHEETS:
		df = dfs[sheet]
		
		for i in range(df.shape[0]):
			var, obj = treatRow(df[i:i+1], list(df), SHEETS[sheet], vars)
			vars[var] = obj
		
		print("[ * ] Table {} remplie.".format(SHEETS[sheet]))
	
	print("\n[ * ] Toutes les données ont bien été insérées.")
			