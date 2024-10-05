# Generated by Django 4.1.5 on 2024-05-20 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0011_alter_invoice_save_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='prix_vente',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=1000),
        ),
        migrations.AddField(
            model_name='article',
            name='remise',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='article',
            name='tva',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='article',
            name='total',
            field=models.DecimalField(decimal_places=3, max_digits=1000),
        ),
        migrations.AlterField(
            model_name='article',
            name='unit_price',
            field=models.DecimalField(decimal_places=3, max_digits=1000),
        ),
    ]
