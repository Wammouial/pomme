from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
    
    return render(request, 'patient.html', {'form': form})

def rep(request):
    return HttpResponse("""
        <h1>Bienvenue sur Pomme</h1>
        <p>Ici c'est la réponse pour le formulaire du patient</p>
        """)
