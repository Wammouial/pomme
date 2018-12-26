from django.contrib.auth import login, authenticate

from .models import Noeud, Personne, Employe, Patient, Specialite, Document, Ecrit, EmpSpe, NoeudSpe

import base64

class BDD(object):
	def _encrypt(self, data):
		"""Encode le paramètre data(str ou bytes) en base64 et retourne
		   l'objet bytes renvoyé."""
		
		if type(data) == str:
			dataBin = data.encode()
		elif type(data) == bytes:
			dataBin = data
		else:
			raise ValueError("Le paramètre data doit être de type str ou bin")

		return base64.b64encode(dataBin)
		
	def _decrypt(self, dataEnc):
		""" Décode le paramètre dataEnc de type bin encodé en base64."""
		
		if type(dataEnc) != bytes:
			raise ValueError("Le paramètre dataStr doit être de type bytes")
		
		return base64.b64decode(dataEnc)
		
	def login(self, username, password):
		"""Verify if the login and the password are good and return the user id if good."""
		