#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.forms import ModelForm

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