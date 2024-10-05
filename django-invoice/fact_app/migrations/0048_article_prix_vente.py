# Generated by Django 4.1.5 on 2024-09-21 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0047_remove_article_prix_vente'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='prix_vente',
            field=models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=10),
        ),
    ]
