
from django import forms

from .models import CheckListItem


class ItemForm(forms.ModelForm[CheckListItem]):
    class Meta:
        model = CheckListItem
        fields = ("description",)
