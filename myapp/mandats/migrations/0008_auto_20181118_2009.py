# Generated by Django 2.1.3 on 2018-11-18 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mandats', '0007_auto_20181118_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comptebancaire',
            name='fournisseur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mandats.Fournisseurs', verbose_name='identifiant proprietaire'),
        ),
    ]
