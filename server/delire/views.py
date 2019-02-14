from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .BDD import BDD
from .forms import PatientForm

# Create your views here.

def form(request): #formulaire patient
    if request.method == 'POST':
        form = PatientForm(request.POST)
        # Nous vérifions que les données envoyées sont valides
        # Cette méthode renvoie False s'il n'y a pas de données
        # dans le formulaire ou qu'il contient des erreurs.
        if form.is_valid():
            # Ici nous pouvons traiter les données du formulaire
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            sexe = form.cleaned_data['sexe']
            date_de_naissance = form.cleaned_data['date_de_naissance']
            numéro_de_securité_sociale = form.cleaned_data['numéro_de_securité_sociale']
            numéro = form.cleaned_data['numéro']
            libellé = form.cleaned_data['libellé']
            code_postal = form.cleaned_data['code_postal']
            ville = form.cleaned_data['ville']
            adresse_email = form.cleaned_data['adresse_email']
            nationalité = form.cleaned_data['nationalité']
            numéro_de_téléphone = form.cleaned_data['numéro_de_téléphone']
            situation_familiale = form.cleaned_data['situation_familiale']
            #message = form.cleaned_data['message']
        
        # Quoiqu'il arrive, on affiche la page du formulaire.
        #return render(request, 'PommeApp/templates/template1.py', locals())
        return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PatientForm()
    
    return render(request, 'formulairepatient.html', {'form': form})

def recherche(request):
    return HttpResponse("""
        <h1>Bienvenue sur Pomme</h1>
        <p>Recherche d'un dossier patient</p>
        """)
		

#DMP
def afficheDocuments(request, pid=""):
	"""Pour l'instant car pas de template"""
	b = BDD()
	
	personne = b.getPersonne(pid)
	if personne is None:
		raise Http404
		
	documents = b.getAllDocument(proprietaire=personne)
	if documents is None:
		return HttpResponse("<p>Aucun document pour cette personne</p>")
		
	result = "<ul>\n"
	for doc in documents:
		result += "<li>" + doc.nom + "</li>\n"
	result += "</ul>"
	
	return HttpResponse(result)