from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['code', 'name', 'quantity', 'unit_price']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data['unit_price']
        if unit_price <= 0:
            raise forms.ValidationError("Unit price must be greater than zero.")
        return 
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['code', 'name', 'quantity', 'unit_price', 'prix']  # Include other fields as needed
