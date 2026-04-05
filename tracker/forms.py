from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-black/30 border border-gray-600 text-white p-3 rounded-lg'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full bg-black/30 border border-gray-600 text-white p-3 rounded-lg'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-black/30 border border-gray-600 text-white p-3 rounded-lg'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full bg-black/30 border border-gray-600 text-white p-3 rounded-lg'
            }),
        }