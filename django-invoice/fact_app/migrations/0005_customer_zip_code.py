# Generated by Django 4.1.5 on 2024-05-17 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0004_remove_customer_sex_remove_customer_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(default='0000', max_length=10),
        ),
    ]