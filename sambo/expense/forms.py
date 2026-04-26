from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm[Expense]):
    class Meta:
        model = Expense
        fields = ("description", "spent_at", "spent_by", "amount")

    def clean_spent_by(self) -> str:
        spent_by = self.cleaned_data.get("spent_by", "").strip().lower()
        assert isinstance(spent_by, str)
        return spent_by
