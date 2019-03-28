#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm, Textarea, TextInput, IntegerField
from django import forms
from .models import Personne

class PatientFormEdit(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PatientFormEdit, self).__init__(*args, **kwargs)
		for f in ('situationFamiliale', 'telephone', 'lieuNaissance'):
			self.fields[f].required = False
			
		for f in self.fields:
			self.fields[f].widget.attrs.update({'class': 'form-control'})
	
	class Meta:
		model = Personne
		fields = ['nom',
				  'prenom',
				  'dateNaissance',
				  'lieuNaissance',
				  'adresse',
				  'telephone',
				  'situationFamiliale',
				  ]
        
class PatientFormCreate(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PatientFormCreate, self).__init__(*args, **kwargs)
		for f in ('situationFamiliale', 'telephone', 'lieuNaissance'):
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
				  'email',
				  ]

class PersonnelFormEdit(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PersonnelFormEdit, self).__init__(*args, **kwargs)
		for f in ('situationFamiliale', 'telephone', 'lieuNaissance'):
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
				  'job',
				  'adresse',
				  'telephone',
				  'situationFamiliale',
				  ]
        
class PersonnelFormCreate(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PersonnelFormCreate, self).__init__(*args, **kwargs)
		for f in ('situationFamiliale', 'telephone', 'lieuNaissance'):
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
				  'job',
				  'adresse',
				  'telephone',
				  'situationFamiliale',
				  'email',
				  ]
		
class RechercheFormPatient(forms.Form):
	nom = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	prenom = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	numSS = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	
class RechercheFormPersonnel(forms.Form):
	nom = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	prenom = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	job = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	
class AddDocumentForm(forms.Form):
	nom = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'form-control'}))
	typeDoc = forms.ChoiceField(choices=[(1, "Diagnostic"), (2, "Ordonnance")])
	date = forms.DateField(input_formats=['%m/%d/%y'], initial="jj/mm/aa")
	fichier = forms.ImageField(max_length=255, allow_empty_file=False)
	brouillon = forms.BooleanField(initial=True, required=False)
	
