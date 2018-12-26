from django.contrib.auth import login, logout, authenticate

from .models import Noeud, Personne, Employe, Patient, Specialite, Document, Ecrit, EmpSpe, NoeudSpe

import base64

class BDD(object):
	TYPE_DOCUMENT = 1
	TYPE_PERSONNE = 2
	TYPE_NOEUD    = 3
	
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
		
	def login(self, username, password, request):
		"""Vérifie si le username et le password sont bons et si oui le connecte dans Django."""
		user = authenticate(request, username, password)
		
		if user is not None:
			login(request, user)
			return True
		
		return False
		
	def getJob(self, idPersonne):
		"""Renvoie le Job"""
		pass
		
	def _getX(self, idX, typeX):
		"""Méthode interne gérant les 3 types de get voulus."""
		if typeX not in (self.TYPE_DOCUMENT, self.TYPE_PERSONNE, self.TYPE_NOEUD):
			raise ValueError("Le paramètre typeX doit être égal à une des 3 contantes de type")
		
		if typeX == self.TYPE_DOCUMENT:
			obj = Document
		elif typeX == self.TYPE_PERSONNE:
			obj = Personne
		else:
			obj = Noeud
			
		try:
			x = obj.objects.get(idX)
		except:
			x = None
		
		return x
		
	def _createX(self, typeX, **kwargs):
		pass
	
	def getDocument(self, id):
		"""Renvoie le document correspondant à l'id donné en paramètre ou None s'il n'est pas dans la BDD"""
		return self._getX(id, self.TYPE_DOCUMENT)
		
	def getPersonne(self, id):
		"""Renvoie la personne correspondant à l'id donné en paramètre ou None si elle n'est pas dans la BDD"""
		return self._getX(id, self.TYPE_PERSONNE)
		
	def getNoeud(self, id):
		"""Renvoie le noeud correspondant à l'id donné en paramètre ou None s'il n'est pas dans la BDD"""
		return self._getX(id, self.TYPE_NOEUD)
	