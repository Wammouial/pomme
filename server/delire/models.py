from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

#Type de Noeud
TYPES_NOEUD = (
	(0, "AP-HP"),
	(1, "Hopital"),
	(2, "Pole"),
	(3, "Service"),
	(4, "Unite-Hospitaliere"),
	(5, "Unite-Soin"),
)

JOBS = (
	(0, "Médecin"),
	(1, "Secrétaire"),
	(2, "DataManager"),
	(3, "Aide-Soignant"),
)

@deconstructible
class PathAndRename(object):
	"""Renommer un fichier avant de l'enregistrer."""

	def __init__(self, sub_path):
		self.path = sub_path

	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		filename = '{}.{}'.format(uuid4().hex, ext)

		return os.path.join(self.path, filename)

class Noeud(models.Model):
	nom = models.CharField(max_length=255)
	type = models.IntegerField(choices=TYPES_NOEUD, default=2)
	pere = models.ForeignKey("Noeud", on_delete=models.CASCADE)
	boss = models.ForeignKey("Employe", on_delete=models.SET_NULL, null=True)

class Personne(User):
	nom = models.CharField(max_length=255)
	prenom = models.CharField(max_length=255)
	dateNaissance = models.DateField()
	lieuNaissance = models.CharField(max_length=500)
	telephone = models.CharField(max_length=14)
	situationFamiliale = models.CharField(max_length=100)
	mail = models.CharField(max_length=255)
	adresse = models.CharField(max_length=500)
	linkedTo = models.ForeignKey(Noeud, on_delete=models.SET_NULL, null=True)
	
class Employe(Personne):
	job = models.IntegerField(choices=JOBS, default=0)
	
	
class Patient(Personne):
	numSS = models.CharField(max_length=15)


class Specialite(models.Model):
	specialite = models.CharField(max_length=255)
	
class Document(models.Model):
	nom = models.CharField(max_length=255)
	date = models.DateField()
	brouillon = models.BooleanField(default=True)
	fichier = models.FileField(upload_to=PathAndRename('documents/'), max_length=200)
	typeDoc = models.CharField(max_length=255)
	proprietaire = models.ForeignKey(Patient, on_delete=models.CASCADE)
	
class Ecrit(models.Model):
	employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
	document = models.ForeignKey(Document, on_delete=models.CASCADE)
	
class EmpSpe(models.Model):
	employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
	specialite = models.ForeignKey(Patient, on_delete=models.CASCADE)
	
class NoeudSpe(models.Model):
	noeud = models.ForeignKey(Noeud, on_delete=models.CASCADE)
	specialite = models.ForeignKey(Patient, on_delete=models.CASCADE)
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	