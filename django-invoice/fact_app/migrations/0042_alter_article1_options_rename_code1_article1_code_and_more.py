# Generated by Django 4.1.5 on 2024-06-09 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0041_article1'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article1',
            options={'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.RenameField(
            model_name='article1',
            old_name='code1',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='article1',
            old_name='name1',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='article1',
            old_name='montant_ht1',
            new_name='prix_vente',
        ),
        migrations.RenameField(
            model_name='article1',
            old_name='quantity1',
            new_name='quantity',
        ),
        migrations.RenameField(
            model_name='article1',
            old_name='montant_ttc1',
            new_name='total',
        ),
        migrations.RenameField(
            model_name='article1',
            old_name='unit_price1',
            new_name='unit_price',
        ),
        migrations.RemoveField(
            model_name='article1',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='article1',
            name='prix_vente1',
        ),
        migrations.RemoveField(
            model_name='article1',
            name='remise1',
        ),
        migrations.RemoveField(
            model_name='article1',
            name='total1',
        ),
        migrations.RemoveField(
            model_name='article1',
            name='tva1',
        ),
    ]