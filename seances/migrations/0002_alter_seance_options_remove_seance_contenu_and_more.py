# Generated by Django 5.0.6 on 2025-03-04 12:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seances', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seance',
            options={'ordering': ['-date', '-heure_debut'], 'verbose_name': 'Séance', 'verbose_name_plural': 'Séances'},
        ),
        migrations.RemoveField(
            model_name='seance',
            name='contenu',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='description',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='duree',
        ),
        migrations.RemoveField(
            model_name='seance',
            name='titre',
        ),
        migrations.AddField(
            model_name='seance',
            name='contenu_seance',
            field=models.TextField(blank=True, help_text='Décrivez le contenu de la séance', verbose_name='Cahier de texte'),
        ),
        migrations.AlterField(
            model_name='presence',
            name='etudiant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seance',
            name='salle',
            field=models.CharField(max_length=50),
        ),
    ]
