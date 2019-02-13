#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
import datetime

class PatientForm(forms.Form):  #formulaire patient modèle ?
    CHOICES=[('select1','F'),
         ('select2','M')]
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    sexe = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    date_de_naissance = forms.DateField(initial=datetime.date.today)
    numéro_de_securité_sociale = forms.CharField(max_length=100)
    numéro = forms.CharField(max_length=3)
    libellé = forms.CharField(max_length=70)
    code_postal = forms.CharField(max_length=5)
    ville = forms.CharField(max_length=100)
    #message = forms.CharField(widget=forms.Textarea)
    adresse_email = forms.EmailField(label="Adresse e-mail")
    nationalité = forms.CharField(max_length=30)
    numéro_de_téléphone = forms.CharField(max_length=10)
    situation_familiale = forms.CharField(max_length=70)
    #renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

