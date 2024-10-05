from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms


class Customer(models.Model):
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    created_date = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name


class Invoice(models.Model):
    INVOICE_TYPE = (
        ('R', _('RECEIPT')),
        ('P', _('PROFORMA INVOICE')),
        ('I', _('INVOICE'))
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, default='DEFAULT_CODE')
    save_by = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    montant_ht = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        date = self.invoice_date_time.date() if self.invoice_date_time else "Unknown Date"
        return f"{self.customer.name}_{date}"

    def update_total(self):
        articles = self.article_set.all()
        self.total = sum(article.total for article in articles)
        self.montant_ht = sum(article.montant_ht for article in articles)
        self.montant_ttc = sum(article.montant_ttc for article in articles)
        self.total_ht = sum(article.montant_ht for article in articles)
        self.total_ttc = sum(article.montant_ttc for article in articles)
        super().save()

    def get_total(self):
        return sum(article.total for article in self.article_set.all())


class Article(models.Model):
    invoice = models.ForeignKey(Invoice, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, default='DEFAULT_CODE')
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    remise = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    tva = models.DecimalField(max_digits=5, decimal_places=3, default=0.000)
    total = models.DecimalField(max_digits=10, decimal_places=3, editable=False, default=0.000)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, editable=False)
    montant_ht = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, editable=False)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, editable=False)
    prix = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, editable=True)
    @property
    def total_tva(self):
        return self.montant_ttc - self.montant_ht

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):
        self.montant_ht = self.quantity * self.unit_price * (1 - self.remise / 100)
        self.montant_ttc = self.montant_ht * (1 + self.tva / 100)
        self.total_ht = sum(self.montant_ht)
        self.total_ttc = sum(self.montant_ttc)
        self.total_tva = self.total_ttc - self.total_ht
        self.total = self.quantity * self.unit_price  # Corrected to ensure it includes tax
        super().save(*args, **kwargs)
        self.invoice.update_total()
        

