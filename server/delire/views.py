from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .BDD import BDD
from .forms import PatientForm

# Create your views here.

def form(request): #formulaire patient
	if request.method == 'POST':
		form = PatientForm(request.POST)

		if form.is_valid():
			nom = form.cleaned_data['nom']
			prenom = form.cleaned_data['prenom']
			sexe = form.cleaned_data['sexe']
			date_de_naissance = form.cleaned_data['dateNaissance']
			lieu_de_naissance = form.cleaned_data['lieuNaissance']
			numero_de_SS = form.cleaned_data['numSS']
			adresse= form.cleaned_data['adresse']
			adresse_email = form.cleaned_data['email']
			téléphone = form.cleaned_data['telephone']
			situation_familiale = form.cleaned_data['situationFamiliale']
			
			
			print("/".join((nom, prenom, lieu_de_naissance, numero_de_SS)))  #Si form valide
		else:
			print(form.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi
		
		return render(request, 'recherchepatient.html', locals())

	else:
		form = PatientForm()
	
	return render(request, 'formulairepatient.html', {'form' : form})

def recherche(request):
	return HttpResponse("""
		<h1>Bienvenue sur Pomme</h1>
		<p>Recherche d'un dossier patient</p>
		""")
		
def rep(request): # Sinon runserver marche pas avec urls.py
	pass
		

#DMP
def afficheDocuments(request, pid=""):
	#Pour l'instant car pas de template
	"""b = BDD()
	
	personne = b.getPersonne(pid)
	if personne is None:
		raise Http404
		
	documents = b.getAllDocument(proprietaire=personne)
	if documents is None or len(documents) == 0:
		return HttpResponse("<p>Aucun document pour cette personne</p>")
		
	result = "<ul>\n"
	for doc in documents:
		result += "<li>" + doc.nom + "</li>\n"
	result += "</ul>"
	
	return HttpResponse(result)"""
	
def editDocument(request, did=""):
	#Toujours pas de template
	"""b = BDD()
	
	doc = b.getDocument(did)
	if doc is None:
		raise Http404
		
	if request.method == "POST":
		pass #A suivre
	"""