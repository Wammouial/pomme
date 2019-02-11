import sys
import pandas
import math
import numpy as np

EXCEL_FILE = "data.xlsx" if len(sys.argv) < 2 else sys.argv[1] 

SHEETS = [ "PersonneClient", "PersonneAPHP", "Noeud", "Spécialité",
		   "Document", "Ecrit", "EmpSpe", "NoeudSpe" ]

def getDF(file, sheet):
	return pandas.read_excel(file, sheet_name=sheet)
	
def treatRow(row, labels, table):
	kwargs = {}
	for y in labels:
		data = row.loc[0, y]
		
		if type(data) == float or type(data) == np.float64:

			if math.isnan(data):
				continue
		kwargs[y] = data
	
	return kwargs

if __name__ == "__main__":
	dfs = {x : getDF(EXCEL_FILE, x) for x in SHEETS}
	
	
	