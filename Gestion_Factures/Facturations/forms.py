# product_manager/forms.py

from django import forms
from .models import Produit
from .models import Client
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['code_article', 'nom_produit', 'prix_unitaire', 'tva']
        labels = {
            'tva': 'TVA (%)',  # Update label for the TVA field
        }
    
    # Add validation for TVA field as a percentage
    def clean_tva(self):
        tva = self.cleaned_data['tva']
        if tva < 0 or tva > 100:
            raise forms.ValidationError("TVA must be between 0 and 100.")
        return tva
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom_client', 'matricule_fiscale', 'contact']
        
from django import forms
from .models import Facturation, Produit
from .models import Client

class ClientSelectForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label=None)

class FacturationForm(forms.ModelForm):
    class Meta:
        model = Facturation
        fields = ['produit', 'quantite', 'prix_unitaire', 'remise', 'tva']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produit'].queryset = Produit.objects.all()