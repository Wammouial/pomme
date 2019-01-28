from django.contrib.auth import login, logout, authenticate

from .models import Noeud, Personne, Specialite, Document, Ecrit, EmpSpe, NoeudSpe, JOBS

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
		personne = self.getPersonne(idPersonne)
		if personne is None:
			return None
			
		return JOBS[personne][1]
		
	def _getX(self, idX, typeX):
		"""Méthode interne gérant les 3 types de get voulus. Renvoie l'objet voulu ou None si erreur."""
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
		"""Méthode interne gérant les 3 types de create voulus."""
		if typeX not in (self.TYPE_DOCUMENT, self.TYPE_PERSONNE, self.TYPE_NOEUD):
			raise ValueError("Le paramètre typeX doit être égal à une des 3 contantes de type")
		
		if typeX == self.TYPE_DOCUMENT:
			obj = Document
			if not ("nom" in kwargs and "date" in kwargs and "brouillon" in kwargs and "fichier" in kwargs and "typeDoc" in kwargs and "proprietaire" in kwargs):
				raise ValueError("Kwargs de createX pour Document mauvais.")
				
			try:
				result = obj.objects.create(nom=kwargs["nom"], date=kwargs["date"], brouillon=kwargs["brouillon"], fichier=kwargs["fichier"],
											typeDoc=kwargs["typeDoc"], proprietaire=kwargs["proprietaire"])
			except Exception as e:
				raise ValueError("Parametres de l'objet à créer invalides : " + repr(e))
		
		elif typeX == self.TYPE_PERSONNE:
			obj = Personne
			if not ("nom" in kwargs and "prenom" in kwargs and "dateNaissance" in kwargs and "lieuNaissance" in kwargs and "telephone" in kwargs \
					and "situationFamiliale" in kwargs and "mail" in kwargs and "adresse" in kwargs and "linkedTo" in kwargs):
				raise ValueError("Kwargs de createX pour Personne mauvais.")
			
			try:
				result = obj.objects.create(nom=kwargs["nom"], prenom=kwargs["prenom"], dateNaissance=kwargs["dateNaissance"], lieuNaissance=kwargs["lieuNaissance"],
											telephone=kwargs["telephone"], situationFamiliale=kwargs["situationFamiliale"], mail=kwargs["mail"],
											adresse=kwargs["adresse"], linkedTo=kwargs["linkedTo"])
			except Exception as e:
				raise ValueError("Parametres de l'objet à créer invalides : " + str(e))
		
		else:
			obj = Noeud
			if not ("nom" in kwargs and "typ" in kwargs and "pere" in kwargs and "boss" in kwargs):
				raise ValueError("Kwargs de createX pour Noeud mauvais.")

			try:
				result = obj.objects.create(nom=kwargs["nom"], typ=kwargs["typ"], pere=kwargs["pere"], boss=kwargs["boss"])
			
			except Exception as e:
				raise ValueError("Parametres de l'objet à créer invalides : " + repr(e))

		return result
		
	def _updateX(self, typeX, idX, **kwargs):
		"""Méthode interne gérant les 3 types de update voulus."""
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
			raise ValueError("idX ne correspond à aucun objet")
		
		for k in kwargs.keys():
			if not hasattr(x, k):
				raise ValueError("L'objet demandé ne possède pas l'attribut " + k)
			
			try:
				setattr(x, k, kwargs[k])
			except:
				raise ValueError("Erreur dans la nouvelle valeur de l'attribut " + k)
		
		try:
			x.save(update_fields=kwargs.keys())
		except:
			raise ValueError("Erreur dans une des nouvelles valeur de l'objet")

	
	def getDocument(self, id):
		"""Renvoie le document correspondant à l'id donné en paramètre ou None s'il n'est pas dans la BDD"""
		return self._getX(id, self.TYPE_DOCUMENT)
		
	def getPersonne(self, id):
		"""Renvoie la personne correspondant à l'id donné en paramètre ou None si elle n'est pas dans la BDD"""
		return self._getX(id, self.TYPE_PERSONNE)
		
	def getNoeud(self, id):
		"""Renvoie le noeud correspondant à l'id donné en paramètre ou None s'il n'est pas dans la BDD"""
		return self._getX(id, self.TYPE_NOEUD)
		
	
	
	def createDocument(self, **kwargs):
		"""Renvoie le document créé si ça a marché ou None si il y a eu un problème"""
		return self._createX(self.TYPE_DOCUMENT, **kwargs)
		
	def createPersonne(self, **kwargs):
		"""Renvoie la personne créée si ça a marché ou None si il y a eu un problème"""
		return self._createX(self.TYPE_PERSONNE, **kwargs)
		
	def createNoeud(self, **kwargs):
		"""Renvoie le noeud créé si ça a marché ou None si il y a eu un problème"""
		return self._createX(self.TYPE_NOEUD, **kwargs)
	
	
	
	def updateDocument(self, id, **kwargs):
		"""Lève une ValueError si l'update n'a pas marché"""
		return self._updateX(self.TYPE_DOCUMENT, id, **kwargs)
		
	def updatePersonne(self, id, **kwargs):
		"""Lève une ValueError si l'update n'a pas marché"""
		return self._updateX(self.TYPE_PERSONNE, id, **kwargs)
		
	def updateNoeud(self, id, **kwargs):
		"""Lève une ValueError si l'update n'a pas marché"""
		return self._updateX(self.TYPE_NOEUD, id, **kwargs)
	