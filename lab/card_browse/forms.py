from django import forms
from .models import Offer
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['user_card', 'quantity', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0: 
            raise forms.ValidationError("Price must be a positive number.") 
        return price
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0: 
            raise forms.ValidationError("Quantity must be a positive number.") 
        return quantity

class SearchForm(forms.Form):

    query = forms.CharField(label = "Search", max_length = 50, required = False)