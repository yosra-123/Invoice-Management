# Generated by Django 4.1.5 on 2024-05-17 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0008_remove_customer_age_remove_customer_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.CharField(default=' ', max_length=12),
        ),
        migrations.AddField(
            model_name='customer',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Feminine')], default=' ', max_length=1),
        ),
    ]
