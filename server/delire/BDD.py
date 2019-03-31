from django.contrib.auth import login, logout, authenticate

from .models import Noeud, Personne, Specialite, Document, Ecrit, EmpSpe, NoeudSpe, JOBS

import base64

class BDD(object):
	TYPE_DOCUMENT = 1
	TYPE_PERSONNE = 2
	TYPE_NOEUD    = 3
	
	def encrypt(self, data):
		"""Encode le paramètre data(str ou bytes) en base64 et retourne
		   l'objet bytes renvoyé."""
		
		if type(data) == str:
			dataBin = data.encode()
		elif type(data) == bytes:
			dataBin = data
		else:
			raise ValueError("Le paramètre data doit être de type str ou bin")

		return base64.b64encode(dataBin)
		
	def decrypt(self, dataEnc):
		""" Décode le paramètre dataEnc de type bin encodé en base64."""
		
		if type(dataEnc) != bytes:
			raise ValueError("Le paramètre dataEnc doit être de type bytes")
		
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
			
		return JOBS[personne.job][1]
		
	def _getX(self, typeX, idX):
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
			x = obj.objects.get(id=idX)
		except:
			x = None
		
		return x
		
	def _getAllX(self, typeX, nResults=-1, **kwargs):
		"""Méthode interne gérant getAll pour les 3 types"""
		if typeX not in (self.TYPE_DOCUMENT, self.TYPE_PERSONNE, self.TYPE_NOEUD):
			raise ValueError("Le paramètre typeX doit être égal à une des 3 contantes de type")
		
		if typeX == self.TYPE_DOCUMENT:
			obj = Document
		elif typeX == self.TYPE_PERSONNE:
			obj = Personne
		else:
			obj = Noeud
			
		try:
			if len(kwargs) > 0:	
				x = obj.objects.filter(**kwargs)
			else:
				x = obj.objects.all()
			
			if nResults >= 0:
				x = x[:nResults]
		
		except Exception as e:
			print("Erreur de getAllX : {}".format(str(e)))
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
				result = obj.objects.create(**kwargs)
			except Exception as e:
				raise ValueError("Parametres de l'objet à créer invalides : " + repr(e))
		
		elif typeX == self.TYPE_PERSONNE:
			obj = Personne
			if not ("nom" in kwargs and "prenom" in kwargs and "dateNaissance" in kwargs and "lieuNaissance" in kwargs and "telephone" in kwargs \
					and "situationFamiliale" in kwargs and "email" in kwargs and "adresse" in kwargs and "linkedTo" in kwargs and "sexe" in kwargs):
				raise ValueError("Kwargs de createX pour Personne mauvais.")
			
			try:
				email = kwargs.pop("email")
				result = obj.objects.create_user(email, **kwargs)
			except Exception as e:
				raise ValueError("Parametres de l'objet à créer invalides : " + str(e))
		
		else:
			obj = Noeud
			if not ("nom" in kwargs and "typ" in kwargs and "pere" in kwargs and "boss" in kwargs):
				raise ValueError("Kwargs de createX pour Noeud mauvais.")

			try:
				result = obj.objects.create(**kwargs)
			
			except Exception as e:
				raise ValueError("Parametres de l'objet à créer invalides : " + repr(e))

		return result
		
	def _updateX(self, x, **kwargs):
		"""Méthode interne gérant les 3 types de update voulus."""
		if type(x) not in (Document, Personne, Noeud):
			raise ValueError("Le paramètre x doit être un objet d'un des 3 types")
		
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
			
	def _deleteX(self, typeX, idX):
		"""Delete l'objet de type et d'id spécifié"""
		if typeX not in (self.TYPE_PERSONNE, self.TYPE_NOEUD):
			raise ValueError("Le paramètre typeX doit être égal à une des 2 contantes de type")
		
		if typeX == self.TYPE_PERSONNE:
			obj = Personne
		else:
			obj = Noeud
		
		try:
			x = obj.objects.get(idX)
		except:
			return False
		
		try:
			x.delete()
		except:
			print("protec fdp")
			return False
		
		return True

	
	def getDocument(self, id):
		"""Renvoie le document correspondant à l'id donné en paramètre ou None s'il n'est pas dans la BDD"""
		return self._getX(self.TYPE_DOCUMENT, id)
		
	def getPersonne(self, id):
		"""Renvoie la personne correspondant à l'id donné en paramètre ou None si elle n'est pas dans la BDD"""
		return self._getX(self.TYPE_PERSONNE, id)
		
	def getNoeud(self, id):
		"""Renvoie le noeud correspondant à l'id donné en paramètre ou None s'il n'est pas dans la BDD"""
		return self._getX(self.TYPE_NOEUD, id)
		
	def getAllDocument(self, nResults=-1, **kwargs):
		"""Renvoie tous les documents de la BDD, si nResults <= 0 renvoie tout sinon renvoie nResults éléments
		   kwargs permet de spécifier des options de filtrage"""
		return self._getAllX(self.TYPE_DOCUMENT, nResults, **kwargs)
		
	def getAllPersonne(self, nResults=-1, **kwargs):
		"""Renvoie toutes les personnes de la BDD, si nResults <= 0 renvoie tout sinon renvoie nResults éléments
		   kwargs permet de spécifier des options de filtrage"""
		return self._getAllX(self.TYPE_PERSONNE, nResults, **kwargs)
		
	def getAllNoeud(self, nResults=-1, **kwargs):
		"""Renvoie tous les noeuds de la BDD, si nResults <= 0 renvoie tout sinon renvoie nResults éléments
		   kwargs permet de spécifier des options de filtrage"""
		return self._getAllX(self.TYPE_NOEUD, nResults, **kwargs)
		
	
	def createDocument(self, **kwargs):
		"""Renvoie le document créé si ça a marché ou None si il y a eu un problème"""
		return self._createX(self.TYPE_DOCUMENT, **kwargs)
		
	def createPersonne(self, **kwargs):
		"""Renvoie la personne créée si ça a marché ou None si il y a eu un problème"""
		return self._createX(self.TYPE_PERSONNE, **kwargs)
		
	def createNoeud(self, **kwargs):
		"""Renvoie le noeud créé si ça a marché ou None si il y a eu un problème"""
		return self._createX(self.TYPE_NOEUD, **kwargs)
	
	
	def updateDocument(self, doc, **kwargs):
		"""Lève une ValueError si l'update n'a pas marché"""
		return self._updateX(doc, **kwargs)
		
	def updatePersonne(self, personne, **kwargs):
		"""Lève une ValueError si l'update n'a pas marché"""
		return self._updateX(personne, **kwargs)
		
	def updateNoeud(self, noeud, **kwargs):
		"""Lève une ValueError si l'update n'a pas marché"""
		return self._updateX(noeud, **kwargs)
		
	
	def deletePersonne(self, id):
		"""Supprime si possible la personne correspondant à cet id"""
		return self._deleteX(self.TYPE_PERSONNE, id)
		
	def deleteNoeud(self, id):
		"""Supprime si possible le noeud correspondant à cet id"""
		return self._deleteX(self.TYPE_NOEUD, id)
	
	
	
	def getNameNoeud(self, idNoeud):
		"""Renvoie le nom du noeud correspondant à idNoeud"""
		try:
			return Noeud.objects.get(idNoeud).nom
		except:
			raise ValueError("idNoeud ne correspond à aucun noeud")
	
	def saveNoeudPersonne(self, idNoeud, idPersonne):
		"""Associe un noeud à une personne même si cette personne est déjà associée à un noeud"""
		try:
			n = Noeud.objects.get(idNoeud)
			p = Personne.objects.get(idPersonne)
		except:
			raise ValueError("Un des id passé en paramètre ne correspond à rien")
			
		try:
			self.updatePersonne(p, linkedTo=n)
		except:
			raise RuntimeError("Impossible d'update linkedTo")
			
	
	
	
	