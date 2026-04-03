from django import forms
from apps.orders.models import Order

DELIVERY_CHOICES = [
    ('Доставка', 'Доставка'),
    ('Самовывоз', 'Самовывоз'),
]

PAYMENT_CHOICES = [
    ('СБП', 'СБП'),
    ('Картой на сайте', 'Картой на сайте'),
]

class OrderCreationForm(forms.ModelForm):
    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = False
        if not args and not kwargs.get('data'):
            self.fields['delivery_method'].initial = 'Самовывоз'
            self.fields['payment_method'].initial = 'СБП'

    class Meta:
        model = Order
        fields = ['client_name', 'client_last_name', 'client_email', 'client_phone', 'address', 'delivery_method', 'payment_method']
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'client_last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'client_email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'client_phone': forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес', 'required': False})
        }