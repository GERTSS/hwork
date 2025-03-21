from django import forms
from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'rating']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'address', 'promocode', 'products']

        widget = {
            'products': forms.CheckboxSelectMultiple,
        }
