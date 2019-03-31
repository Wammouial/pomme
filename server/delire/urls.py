"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', lambda request: redirect('searchPatient', permanent=False)),
	path('login', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
	path('logout', auth_views.LogoutView.as_view(), name='logout'),
	path('createPatient', views.formPatient, name="createPatient"),
    path('updatePatient/<int:idPersonne>', views.modifierPatient, name="updatePatient"),
    path('searchPatient', views.recherchePatient, name="searchPatient"),
    path('createPersonnel', views.formPersonnel, name="createPersonnel"),
    path('updatePersonnel/<int:idPersonne>', views.modifierPersonnel, name="updatePersonnel"),
    path('searchPersonnel', views.recherchePersonnel, name="searchPersonnel"),
	path('afficheDocuments/<int:pid>', views.afficheDocuments, name="afficheDocs"),
	path('editDocument/<int:did>', views.editDocument, name="editDoc"),
	path('seeDmp/<int:pid>', views.afficheDocuments, name="dmp"),
]
