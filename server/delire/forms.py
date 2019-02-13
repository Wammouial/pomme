#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models
from django.forms import ModelForm

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
    
class PatientForm(ModelForm):
    class Meta:
        model = Profil
        fields = ['nom',
                  'prenom',
                  'date_de_naissance',
                  'sexe',
                  'numéro_de_sécurité_sociale',
                  'numéro',
                  'libellé',
                  'code_postal',
                  'ville',
                  'adresse_email',
                  'nationalité',
                  'numéro_de_téléphone',
                  'situation_familiale']