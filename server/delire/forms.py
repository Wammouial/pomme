#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea, TextInput
from django import forms
from .models import Personne

class PatientForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PatientForm, self).__init__(*args, **kwargs)
		for f in ('numSS', 'situationFamiliale', 'telephone', 'lieuNaissance'):
			self.fields[f].required = False
			
		for f in self.fields:
			self.fields[f].widget.attrs.update({'class': 'form-control'})
	
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
				  'situationFamiliale',
				  ]
		
class RechercheForm(forms.Form):
	nom = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	prenom = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	numSS = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	