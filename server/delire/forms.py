#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from django import forms
from .models import Personne

class PatientForm(ModelForm):
    class Meta:
        model = Personne
        fields = ['nom',
				  'prenom',
                  'sexe',
				  'dateNaissance',
				  'lieuNaissance',
                  'numSS',
                  'adresse',
				  'telephone',
                  'email',
				  'situationFamiliale',
				  ]
        
class RechercheForm(forms.Form):
        nom = forms.CharField(max_length=255)
        prenom = forms.CharField(max_length=255, required=False)
        numSS = forms.CharField(max_length=15, required=False)