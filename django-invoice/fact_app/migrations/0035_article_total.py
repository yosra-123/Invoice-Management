# Generated by Django 4.1.5 on 2024-06-01 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0034_remove_article_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='total',
            field=models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=10),
        ),
    ]
