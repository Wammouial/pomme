from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .BDD import BDD
from .forms import PatientFormEdit, PatientFormCreate, RechercheFormPatient, RechercheFormPersonnel, PersonnelFormEdit, PersonnelFormCreate, AddDocumentForm
from .models import getJobByNumber, Document

import types
from PIL import Image


def rightsRequired(*args1):
	def wrap(f):
		def decorate(request, *args, **kwargs):
			if request.user.job not in args1:
				raise PermissionDenied
			return f(request, *args, **kwargs)
		return decorate
	return wrap

@login_required
def formPatient(request): #formulaire patient
	if request.method == 'POST':
		form = PatientFormCreate(request.POST)

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

		return redirect('/pomme/searchPatient')

	else:
		form = PatientFormCreate()
	
	return render(request, 'formulairepatient.html', {'form' : form})

@login_required
@rightsRequired(2)
def formPersonnel(request): #formulaire patient
	if request.method == 'POST':
		form = PersonnelFormCreate(request.POST)

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
			job = form.cleaned_data['job'] #getJobByNumber(form.cleaned_data['job'])
			adresse= form.cleaned_data['adresse']
			adresse_email = form.cleaned_data['email']
			téléphone = form.cleaned_data['telephone']
			situation_familiale = form.cleaned_data['situationFamiliale']

			#create
			b = BDD()
			b.createPersonne(job=job, numSS=None,
							nom=nom,
							prenom=prenom,
							sexe=sexe,
							dateNaissance=date_de_naissance,
							lieuNaissance=lieu_de_naissance,
							adresse=adresse,
							email=adresse_email,
							telephone=téléphone,
							situationFamiliale=situation_familiale,
							linkedTo=None)
			messages.success(request, 'Personnel crée.')
		else:
			print(form.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi

		return redirect('/pomme/searchPersonnel')

	else:
		form = PersonnelFormCreate()
	
	return render(request, 'formulairepersonnel.html', {'form' : form})

@login_required
def modifierPatient(request, idPersonne): #formulaire patient
	b = BDD()
	identite = b.getPersonne(idPersonne)
	
	if request.method == 'POST':
		mod = PatientFormEdit(request.POST)

		if mod.is_valid():
			#update
			b.updatePersonne(identite, **mod.cleaned_data)
			messages.success(request, 'Modification effectuée avec succès.')

		else:
			print(mod.errors.as_data())	 #Affiche dans la console les champs en erreur et pourquoi
		
		return redirect('/pomme/searchPatient')

	else:
		dico = {'nom': identite.nom,
			   'prenom':identite.prenom,
			   'dateNaissance':identite.dateNaissance,
			   'lieuNaissance':identite.lieuNaissance,
			   'adresse':identite.adresse,
			   'email':identite.email,
			   'telephone':identite.telephone,
			   'situationFamiliale':identite.situationFamiliale,
			   }
		numSS = identite.numSS
		if(identite.sexe=="M"):
			sexe = 'Masculin'
		else:
			sexe = 'Féminin'


		mod = PatientFormEdit(initial=dico)
	print(locals())
	return render(request, 'formulairemodifpatient.html', locals())

@login_required
@rightsRequired(2)
def modifierPersonnel(request, idPersonne): #formulaire patient
	b = BDD()
	identite = b.getPersonne(idPersonne)

	if request.method == 'POST':
		mod = PersonnelFormEdit(request.POST)

		if mod.is_valid():
			#update
			b.updatePersonne(identite, **mod.cleaned_data)
			messages.success(request, 'Modification effectuée avec succès.')

		else:
			print(mod.errors.as_data())	 #Affiche dans la console les champs en erreur et pourquoi
		
		return redirect('/pomme/searchPersonnel')

	else:
		print(identite.job)
		dico = {'nom': identite.nom,
			   'prenom':identite.prenom,
			   'sexe':identite.sexe,
			   'dateNaissance':identite.dateNaissance,
			   'lieuNaissance':identite.lieuNaissance,
			   'job':identite.job, #verif et numSS ?
			   'adresse':identite.adresse,
			   'email':identite.email,
			   'telephone':identite.telephone,
			   'situationFamiliale':identite.situationFamiliale,
			   }

		if(identite.sexe=="M"):
			sexe = 'Masculin'
		else:
			sexe = 'Féminin'
		mod = PersonnelFormEdit(initial=dico)
	
	return render(request, 'formulairemodifpersonnel.html', {'mod' : mod})

@login_required
def recherchePatient(request):
	formu = RechercheFormPatient(request.GET)

	if formu.is_valid():
		nom = formu.cleaned_data['nom']
		prenom = formu.cleaned_data['prenom']
		numSS = formu.cleaned_data['numSS']
		b = BDD()
		if prenom!='' and numSS!='': #si on trouve du premier coup
			patients = b.getAllPersonne(job=0, nom=nom, prenom=prenom, numSS=numSS)
		elif prenom!='' and numSS=='':
			patients = b.getAllPersonne(job=0, nom=nom, prenom=prenom)
		elif prenom=='' and numSS!='':
			patients = b.getAllPersonne(job=0, nom=nom, numSS=numSS)
		else: #prenom=='' and numSS==''
			patients = b.getAllPersonne(job=0, nom=nom)
		if not(patients): #si on ne trouve pas du premier coup dans la BDD
			liste = b.getAllPersonne(job=0)
			taille = len(liste)
			patients = []
			found = False
			nom = nom.lower()
			prenom = prenom.lower()
			if prenom!='' and numSS!='':
				for i in range(0,taille):
					if nom in liste[i].nom.lower() and prenom in liste[i].prenom.lower() and numSS in liste[i].numSS:
						patients.append(liste[i])
						found=True
			elif prenom!='' and numSS=='':
				for i in range(0,taille):
					if nom in liste[i].nom.lower() and prenom in liste[i].prenom.lower():
						patients.append(liste[i])
						found=True
			elif prenom=='' and numSS!='':
				for i in range(0,taille):
					if nom in liste[i].nom.lower() and numSS in liste[i].numSS:
						patients.append(liste[i])
						found=True
			else: #prenom=='' and numSS==''
				for i in range(0,taille):
					if nom in liste[i].nom.lower(): #si lettre en trop
						patients.append(liste[i])
						found=True
			if found==False:
				messages.error(request, 'Aucun patient correspondant à ces critères de recherche n’a été trouvé.')
		
		return render(request, 'recherchepatient.html', locals())
	
	
	else:
		formu = RechercheFormPatient()
		b = BDD()
		patients = b.getAllPersonne(job=0)
	
	return render(request, 'recherchepatient.html', locals())

@login_required
@rightsRequired(2)
def recherchePersonnel(request):
	formu = RechercheFormPersonnel(request.GET)
	affiliation1 = "Secrétaire"
	affiliation2 = "DataManager"
	affiliation3 = "Aide-Soignant"
	affiliation4 = "Médecin"

	if formu.is_valid():
		nom = formu.cleaned_data['nom']
		prenom = formu.cleaned_data['prenom']
		b = BDD()
		if nom!='' and prenom!='':
			personnels = b.getAllPersonne(nom=nom, prenom=prenom)
		else:
			personnels = b.getAllPersonne(nom=nom)
		if not(personnels): #si on ne trouve pas du premier coup dans la BDD
			liste = b.getAllPersonne()
			taille = len(liste)
			personnels = []
			found = False
			nom = nom.lower()
			prenom = prenom.lower()
			if nom!='' and prenom!='':
				for i in range(0,taille):
					if nom in liste[i].nom.lower() and prenom in liste[i].prenom.lower():
						personnels.append(liste[i])
						found=True
			else: #prenom==''
				for i in range(0,taille):
					if nom in liste[i].nom.lower(): #si lettre en trop
						personnels.append(liste[i])
						found=True
			if found==False:
				messages.error(request, 'Aucun personnel correspondant à ces critères de recherche n’a été trouvé.')
			
			postTaille = len(personnels)
			for i in range(0,postTaille):
				if personnels[i].job == 0:
					personnels.remove(personnels[i])

		return render(request, 'recherchepersonnel.html', locals())

	else:
		formu = RechercheFormPersonnel()
		b = BDD()
		liste = b.getAllPersonne()
		taille = len(liste)
		personnels = []
		for i in range(0,taille):
			if not (liste[i].job == 0):
				personnels.append(liste[i])
	
	return render(request, 'recherchepersonnel.html', locals())

@login_required	
def rep(request): # Sinon runserver marche pas avec urls.py
	pass
		

#DMP
@login_required
@rightsRequired(1, 4)
def afficheDocuments(request, pid=""):	
	b = BDD()
	
	personne = b.getPersonne(pid)
	if personne is None:
		raise Http404
		
	documents = b.getAllDocument(proprietaire=personne)
	
	ordos = [doc for doc in documents if doc.typeDoc == "Ordonnance"]
	diagnos = [doc for doc in documents if doc.typeDoc == "Diagnostic"]
	
	pnameSurname = personne.get_full_name()
	
	if request.method == "POST":
		form = AddDocumentForm(request.POST, request.FILES)
		
		if form.is_valid():
			nom = form.cleaned_data["nom"]
			date = form.cleaned_data["date"]
			brouillon = form.cleaned_data["brouillon"]
			
			typeDoc = form.cleaned_data["typeDoc"]
			typeDoc = "Diagnostic" if typeDoc == 1 else "Ordonnance"
			
			fichier = Image.open(form.cleaned_data["fichier"])
			
			fichier = Document.imgToB64(fichier)
			
			doc = b.createDocument(nom=nom, typeDoc=typeDoc, date=date, brouillon=brouillon, fichier=fichier, proprietaire=personne)
			return redirect("editDoc", doc.id)
		
		else:
			print(form.errors.as_data())
			
	else:
		form = AddDocumentForm()
	
	return render(request, 'dmp.html', locals())

@login_required
@rightsRequired(1, 4)
def editDocument(request, did=""):
	b = BDD()
	
	doc = b.getDocument(did)
	if doc is None:
		raise Http404
		
	patient = doc.proprietaire
	
	return render(request, 'dmpM.html', locals())

	
def getImports(request):
	"""Pas touche minouche"""
	l = []
	
	for name, val in globals().items():
		if isinstance(val, types.ModuleType):
			l.append(val.__name__)
			
	p = "<ul>"
	for modu in l:
		p += "\n<li>" + modu + "</li>"
	p += "\n</ul>"
	
	return HttpResponse(p)
