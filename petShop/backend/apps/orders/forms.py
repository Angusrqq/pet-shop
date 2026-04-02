from django import forms
from apps.orders.models import Order

class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'client_last_name', 'client_email', 'client_phone', 'address']
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'client_last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'client_email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'client_phone': forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес'})
        }