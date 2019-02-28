from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .BDD import BDD
from .forms import PatientForm, RechercheForm

# Create your views here.

def form(request): #formulaire patient
	if request.method == 'POST':
		form = PatientForm(request.POST)

		if form.is_valid():
			nom = form.cleaned_data['nom']
			prenom = form.cleaned_data['prenom']
			sexe = form.cleaned_data['sexe']
			#if sexe == 'F':
				#sexe = 1
			#else:
				#sexe = 0
			date_de_naissance = form.cleaned_data['dateNaissance']
			lieu_de_naissance = form.cleaned_data['lieuNaissance']
			numero_de_SS = form.cleaned_data['numSS']
			adresse= form.cleaned_data['adresse']
			adresse_email = form.cleaned_data['email']
			téléphone = form.cleaned_data['telephone']
			situation_familiale = form.cleaned_data['situationFamiliale']
			
			#create
			print("/".join((nom, prenom, lieu_de_naissance, numero_de_SS)))  #Si form valide
		else:
			print(form.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi
		
		return render(request, 'formulairepatient.html', locals())
		# return render(request, 'recherchepatient.html', locals())  // Pas bon
		
		# La vue form attachée à path('formpatient', views.form, name="formpatient") dans urls.py
		# ne peut retourner que son propre template et non pas celui de recherche qui est
		# recherchepatient.html. Si tu veux que le contenu du formulaire aille dans une autre
		# vue tu dois mettre dans l'action du form l'url qui va lancer l'autre vue
		# Genre <form class="form-login" action="{% url 'reppatient' %}" method="post">
		# Et là ça t'enverra bien ce que tu veux où tu veux

	else:
		form = PatientForm()
	
	return render(request, 'formulairepatient.html', {'form' : form})

def recherche(request):
	if request.method == 'POST':
		formu = RechercheForm(request.POST)

		if formu.is_valid():
			nom = formu.cleaned_data['nom']
			prenom = formu.cleaned_data['prenom']
			b = BDD()
			if prenom!='':
				patients = b.getAllPersonne(job=0, nom=nom, prenom=prenom)
			else:
				patients = b.getAllPersonne(job=0, nom=nom)
			print(patients)
			
			return render(request, 'recherchepatient.html', locals())
			
			# return render(request, 'recherchepatient.html', locals(), {'liste': patients}) // Pas bon
			
			# Faut faire soit locals() soit {'liste': 'patients'}, les deux ça n'a pas de sens 

		else:
			print(formu.errors.as_data())
		return render(request, 'recherchepatient.html')

	else:
		formu = RechercheForm()
	
	return render(request, 'recherchepatient.html', locals())
		
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