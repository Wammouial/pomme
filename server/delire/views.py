from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
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
			if sexe == 'F':
				sexe = 1
			else:
				sexe = 0
			date_de_naissance = form.cleaned_data['dateNaissance']
			lieu_de_naissance = form.cleaned_data['lieuNaissance']
			numero_de_SS = form.cleaned_data['numSS']
			adresse= form.cleaned_data['adresse']
			adresse_email = form.cleaned_data['email']
			téléphone = form.cleaned_data['telephone']
			situation_familiale = form.cleaned_data['situationFamiliale']

			#if not (numero_de_SS.startswith('1') and sexe==1):
				#raise form.ValidationError(form.error_messages['Impossible.'])

			#create
			b = BDD()
			b.createPersonne(job=0, nom=nom,
							prenom=prenom,
							sexe=sexe,
							dateNaissance=date_de_naissance,
							lieuNaissance=lieu_de_naissance,
							numSS=numero_de_SS,
							adresse=adresse,
							email=adresse_email,
							telephone=téléphone,
							situationFamiliale=situation_familiale,
							linkedTo=None)
			messages.success(request, 'Patient crée.')
		else:
			print(form.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi
		
		#return render(request, 'formulairepatient.html', locals())

		return redirect('/pomme/searchPatient')

	else:
		form = PatientForm()
	
	return render(request, 'formulairepatient.html', {'form' : form})

def modifierPatient(request, idPersonne, nom): #formulaire patient
	if request.method == 'POST':
		b = BDD()
		identite = b.getPersonne(idPersonne)
		mod = PatientForm(request.POST,initial=identite.nom)

		if mod.is_valid():

			#mod.fields['nom'].initial = identite.nom
			nom = mod.cleaned_data['nom']
			prenom = mod.cleaned_data['prenom']
			sexe = mod.cleaned_data['sexe']
			if sexe == 'F':
				sexe = 1
			else:
				sexe = 0
			date_de_naissance = mod.cleaned_data['dateNaissance']
			lieu_de_naissance = mod.cleaned_data['lieuNaissance']
			numero_de_SS = mod.cleaned_data['numSS']
			adresse= mod.cleaned_data['adresse']
			adresse_email = mod.cleaned_data['email']
			téléphone = mod.cleaned_data['telephone']
			situation_familiale = mod.cleaned_data['situationFamiliale']
			#update
			b.updatePersonne(identite, nom=nom,
							prenom=prenom,
							sexe=sexe,
							dateNaissance=date_de_naissance,
							lieuNaissance=lieu_de_naissance,
							numSS=numero_de_SS,
							adresse=adresse,
							email=adresse_email,
							telephone=téléphone,
							situationFamiliale=situation_familiale,
							linkedTo=None)
			print(id)
		else:
			print(mod.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi
		
		return redirect('/pomme/searchPatient')

	else:
		mod = PatientForm()
	
	return render(request, 'formulairemodifpatient.html', {'mod' : mod})
"""def modifierPatient(request, idPersonne): #formulaire patient
	message = "Le nom de l'album est {}.".format(idPersonne)
	return HttpResponse(message)"""

def recherche(request):
	if request.method == 'POST':
		formu = RechercheForm(request.POST)

		if formu.is_valid():
			nom = formu.cleaned_data['nom']
			prenom = formu.cleaned_data['prenom']
			numSS = formu.cleaned_data['numSS']
			b = BDD()
			if prenom!='' and numSS!='':
				patients = b.getAllPersonne(job=0, nom=nom, prenom=prenom, numSS=numSS)
			elif prenom!='' and numSS=='':
				patients = b.getAllPersonne(job=0, nom=nom, prenom=prenom)
			elif prenom=='' and numSS!='':
				patients = b.getAllPersonne(job=0, nom=nom, numSS=numSS)
			else: #prenom=='' and numSS==''
				patients = b.getAllPersonne(job=0, nom=nom)
			if not(patients):
				messages.error(request, 'Aucun patient correspondant à ces critères de recherche n’a été trouvé.')
			
			return render(request, 'recherchepatient.html', locals())
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