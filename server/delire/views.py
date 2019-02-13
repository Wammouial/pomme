from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from BDD import BDD
from .forms import ContactForm

# Create your views here.

def form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # Nous vérifions que les données envoyées sont valides
        # Cette méthode renvoie False s'il n'y a pas de données
        # dans le formulaire ou qu'il contient des erreurs.
        if form.is_valid():
            # Ici nous pouvons traiter les données du formulaire
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            envoyeur = form.cleaned_data['envoyeur']
            renvoi = form.cleaned_data['renvoi']
            
            # Nous pourrions ici envoyer l'e-mail grâce aux données
            # que nous venons de récupérer
            envoi = True
        
        # Quoiqu'il arrive, on affiche la page du formulaire.
        #return render(request, 'PommeApp/templates/template1.py', locals())
        return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    
    return render(request, 'patient.html', {'form': form})

def rep(request):
    return HttpResponse("""
        <h1>Bienvenue sur Pomme</h1>
        <p>Ici c'est la réponse pour le formulaire du patient</p>
        """)
