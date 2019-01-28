from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

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
	(0, "Patient"),
	(1, "Secrétaire"),
	(2, "DataManager"),
	(3, "Aide-Soignant"),
	(4, "Médecin"),
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
		
class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

class Noeud(models.Model):
	nom = models.CharField(max_length=255)
	typ = models.IntegerField(choices=TYPES_NOEUD, default=2)
	pere = models.ForeignKey("Noeud", on_delete=models.CASCADE)	 #selfRef
	boss = models.ForeignKey("Personne", on_delete=models.SET_NULL, null=True)

class Personne(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True)
	nom = models.CharField(max_length=255)
	prenom = models.CharField(max_length=255)
	dateNaissance = models.DateField()
	lieuNaissance = models.CharField(max_length=500)
	telephone = models.CharField(max_length=14)
	situationFamiliale = models.CharField(max_length=100)
	adresse = models.CharField(max_length=500)
	linkedTo = models.ForeignKey(Noeud, on_delete=models.SET_NULL, null=True)
	job = models.IntegerField(choices=JOBS, default=0)
	numSS = models.CharField(max_length=15, null=True)
	is_active = models.BooleanField(default=True)
	
	objects = UserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	class Meta:
		verbose_name = 'personne'
		verbose_name_plural = 'personnes'

	def get_full_name(self):
		full_name = '%s %s' % (self.prenom, self.nom)
		return full_name.strip()

	def get_short_name(self):
		return self.prenom

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)
	
	
class Specialite(models.Model):
	specialite = models.CharField(max_length=255)
	
class Document(models.Model):
	nom = models.CharField(max_length=255)
	date = models.DateField()
	brouillon = models.BooleanField(default=True)
	fichier = models.FileField(upload_to=PathAndRename('documents/'), max_length=200)
	typeDoc = models.CharField(max_length=255)
	proprietaire = models.ForeignKey(Personne, on_delete=models.CASCADE)
	
class Ecrit(models.Model):
	employe = models.ForeignKey(Personne, on_delete=models.CASCADE)
	document = models.ForeignKey(Document, on_delete=models.CASCADE)
	
class EmpSpe(models.Model):
	employe = models.ForeignKey(Personne, on_delete=models.CASCADE)
	specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)
	
class NoeudSpe(models.Model):
	noeud = models.ForeignKey(Noeud, on_delete=models.CASCADE)
	specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)	
	