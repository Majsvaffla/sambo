from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm[Expense]):
    class Meta:
        model = Expense
        fields = ("description", "spent_at", "paid_by", "amount")

    def clean_paid_by(self) -> str:
        paid_by = self.cleaned_data.get("paid_by", "").strip().lower()
        assert isinstance(paid_by, str)
        return paid_by
