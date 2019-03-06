from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .BDD import BDD
from .forms import PatientFormEdit, PatientFormCreate, RechercheFormPatient, RechercheFormPersonnel, PersonnelFormEdit, PersonnelFormCreate

# Create your views here.

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

        return redirect('/pomme/searchPatient')

    else:
        form = PatientFormCreate()
    
    return render(request, 'formulairepatient.html', {'form' : form})

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
            job = form.cleaned_data['job']
            adresse= form.cleaned_data['adresse']
            adresse_email = form.cleaned_data['email']
            téléphone = form.cleaned_data['telephone']
            situation_familiale = form.cleaned_data['situationFamiliale']

            #create
            b = BDD()
            b.createPersonne(job=job,
                            nom=nom,
                            prenom=prenom,
                            sexe=sexe,
                            dateNaissance=date_de_naissance,
                            lieuNaissance=lieu_de_naissance,
                            numSS="",
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
            print(mod.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi
        
        return redirect('/pomme/searchPatient')

    else:
        print(identite.numSS)
        dico = {'nom': identite.nom,
               'prenom':identite.prenom,
               'sexe':identite.sexe,
               'dateNaissance':identite.dateNaissance,
               'lieuNaissance':identite.lieuNaissance,
               'numSS':identite.numSS,
               'adresse':identite.adresse,
               'email':identite.email,
               'telephone':identite.telephone,
               'situationFamiliale':identite.situationFamiliale,
               }

        mod = PatientFormEdit(initial=dico)
    
    return render(request, 'formulairemodifpatient.html', {'mod' : mod})


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
            print(mod.errors.as_data())  #Affiche dans la console les champs en erreur et pourquoi
        
        return redirect('/pomme/searchPersonnel')

    else:
        print(identite.job)
        dico = {'nom': identite.nom,
               'prenom':identite.prenom,
               'sexe':identite.sexe,
               'dateNaissance':identite.dateNaissance,
               'lieuNaissance':identite.lieuNaissance,
               'job':identite.job,
               'adresse':identite.adresse,
               'email':identite.email,
               'telephone':identite.telephone,
               'situationFamiliale':identite.situationFamiliale,
               }

        mod = PersonnelFormEdit(initial=dico)
    
    return render(request, 'formulairemodifpersonnel.html', {'mod' : mod})

def recherchePatient(request):
    formu = RechercheFormPatient(request.GET)

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
        formu = RechercheFormPatient()
    
    return render(request, 'recherchepatient.html', locals())

def recherchePersonnel(request):
    formu = RechercheFormPersonnel(request.GET)

    if formu.is_valid():
        nom = formu.cleaned_data['nom']
        prenom = formu.cleaned_data['prenom']
        job = formu.cleaned_data['job']
        b = BDD()
        if prenom!='' and job!='':
            personnels = b.getAllPersonne(numSS=0, nom=nom, prenom=prenom, job=job)
        elif prenom!='' and job=='':
            personnels = b.getAllPersonne(numSS=0, nom=nom, prenom=prenom)
        elif prenom=='' and job!='':
            personnels = b.getAllPersonne(numSS=0, nom=nom, job=job)
        else: #prenom=='' and job==''
            personnels = b.getAllPersonne(numSS=0, nom=nom)
        if not(personnels):
            messages.error(request, 'Aucun personnel correspondant à ces critères de recherche n’a été trouvé.')
        
        return render(request, 'recherchepersonnel.html', locals())
    
    
    else:
        formu = RechercheFormPersonnel()
    
    return render(request, 'recherchepersonnel.html', locals())
        
def rep(request): # Sinon runserver marche pas avec urls.py
    pass
        

#DMP
def afficheDocuments(request, pid=""):
    #Pour l'instant car pas de template
    b = BDD()
    
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
    
    return HttpResponse(result)
    
def editDocument(request, did=""):
    #Toujours pas de template
    """b = BDD()
    
    doc = b.getDocument(did)
    if doc is None:
        raise Http404
        
    if request.method == "POST":
        pass #A suivre
    """
