#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.forms import ModelForm

from .models import Personne

# Je te laisse supprimer ça, ça fait mal de supprimer tout ce travail
"""
CHOICES=[('select1','Féminin'),
         ('select2','Masculin')]

class Profil(models.Model):  #formulaire patient modèle ?
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=2, choices=CHOICES)
    date_de_naissance = models.DateField(blank=True, null=True)
    numéro_de_sécurité_sociale = models.CharField(max_length=100)
    numéro = models.CharField(max_length=3)
    libellé = models.CharField(max_length=70)
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)
    adresse_email = models.EmailField(max_length=70)
    nationalité = models.CharField(max_length=30)
    numéro_de_téléphone = models.CharField(max_length=10)
    situation_familiale = models.CharField(max_length=70)
   
"""

class PatientForm(ModelForm):
    class Meta:
        model = Personne
        fields = ['email',
				  'nom',
				  'prenom',
                  'sexe',
				  'dateNaissance',
				  'lieuNaissance',
				  'telephone',
				  'situationFamiliale',
				  'adresse',
				  'numSS',
				  ]