# Generated by Django 4.1.5 on 2024-05-25 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0022_alter_article_montant_ht_alter_article_montant_ttc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='zip_code',
        ),
    ]