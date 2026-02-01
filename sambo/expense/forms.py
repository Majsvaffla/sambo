from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm[Expense]):
    class Meta:
        model = Expense
        fields = ("description", "spent_at", "amount")
