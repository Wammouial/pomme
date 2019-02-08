# Generated by Django 2.0.5 on 2019-02-08 08:16

import delire.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('dateNaissance', models.DateField()),
                ('lieuNaissance', models.CharField(max_length=500)),
                ('telephone', models.CharField(max_length=14)),
                ('situationFamiliale', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=500)),
                ('job', models.IntegerField(choices=[(0, 'Patient'), (1, 'Secrétaire'), (2, 'DataManager'), (3, 'Aide-Soignant'), (4, 'Médecin')], default=0)),
                ('numSS', models.CharField(max_length=15, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'personne',
                'verbose_name_plural': 'personnes',
            },
            managers=[
                ('objects', delire.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('brouillon', models.BooleanField(default=True)),
                ('fichier', models.FileField(max_length=200, upload_to=delire.models.PathAndRename('documents/'))),
                ('typeDoc', models.CharField(max_length=255)),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ecrit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delire.Document')),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmpSpe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Noeud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('typ', models.IntegerField(choices=[(0, 'AP-HP'), (1, 'Hopital'), (2, 'Pole'), (3, 'Service'), (4, 'Unite-Hospitaliere'), (5, 'Unite-Soin')], default=2)),
                ('boss', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('pere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delire.Noeud')),
            ],
        ),
        migrations.CreateModel(
            name='NoeudSpe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noeud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delire.Noeud')),
            ],
        ),
        migrations.CreateModel(
            name='Specialite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialite', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='noeudspe',
            name='specialite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delire.Specialite'),
        ),
        migrations.AddField(
            model_name='empspe',
            name='specialite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delire.Specialite'),
        ),
        migrations.AddField(
            model_name='personne',
            name='linkedTo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='delire.Noeud'),
        ),
        migrations.AddField(
            model_name='personne',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
