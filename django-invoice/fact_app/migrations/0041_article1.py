# Generated by Django 4.1.5 on 2024-06-09 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0040_alter_article_invoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code1', models.CharField(default='DEFAULT_CODE', max_length=32)),
                ('name1', models.CharField(max_length=32)),
                ('quantity1', models.IntegerField()),
                ('unit_price1', models.DecimalField(decimal_places=3, max_digits=10)),
                ('remise1', models.DecimalField(decimal_places=3, default=0, max_digits=5)),
                ('tva1', models.DecimalField(decimal_places=3, default=0.0, max_digits=5)),
                ('total1', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=10)),
                ('prix_vente1', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=10)),
                ('montant_ht1', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=10)),
                ('montant_ttc1', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=10)),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fact_app.invoice')),
            ],
            options={
                'verbose_name': 'Article1',
                'verbose_name_plural': 'Articles1',
            },
        ),
    ]
