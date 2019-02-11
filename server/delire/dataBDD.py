import sys
import pandas

EXCEL_FILE = "data.xlsx" if len(sys.argv) < 2 else sys.argv[1] 

SHEETS = [ "PersonneClient", "PersonneAPHP", "Noeud", "Spécialité",
		   "Document", "Ecrit", "EmpSpe", "NoeudSpe" ]

def getDF(file, sheet):
	return pandas.read_excel(file, sheet_name=sheet)

if __name__ == "__main__":
	dfs = {x : getDF(EXCEL_FILE, x) for x in SHEETS}
	
	