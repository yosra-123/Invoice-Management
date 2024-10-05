from django.db import models
from decimal import Decimal

class Produit(models.Model):
    code_article = models.CharField(max_length=20, unique=True)
    nom_produit = models.CharField(max_length=100)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'))  # Ensure proper decimal format
    tva = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='TVA (%)', default=Decimal('0.00'))  # Add default value

    def __str__(self):
        return self.nom_produit

class Client(models.Model):
    nom_client = models.CharField(max_length=100)
    matricule_fiscale = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_client

class Facturation(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=3, default=Decimal('0.000'))  # Ensure proper decimal format
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))  # Ensure proper decimal format
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))  # Ensure proper decimal format
    montant_htva = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default=Decimal('0.00'))  # Ensure proper decimal format
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, default=Decimal('0.00'))  # Ensure proper decimal format
    
    def save(self, *args, **kwargs):
        self.montant_htva = self.quantite * self.produit.prix_unitaire * (1 - self.remise / 100)
        self.montant_ttc = self.montant_htva * (1 + self.produit.tva / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Facture {self.produit.nom_produit} - {self.id}"
