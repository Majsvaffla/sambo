from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.contrib import admin

from sambo.admin import site
from sambo.components import details_url

from .formatters import format_money
from .models import Bill, Expense

if TYPE_CHECKING:
    import htpy as h


class ExpenseInline(admin.TabularInline[Expense, Bill]):
    model = Expense
    fields = ["description", "amount", "spent_at", "settled_at"]
    extra = 0


@admin.register(Bill, site=site)
class BillAdmin(admin.ModelAdmin[Bill]):
    list_display = [
        "name",
        "admin_url",
        "admin_total_amount",
    ]
    fields = ["name"]
    inlines = [ExpenseInline]

    @admin.display(description="URL")
    def admin_url(self, instance: Bill) -> h.Element:
        return details_url(instance, title="Visa nota", url_pattern_name="bill")

    @admin.display(description="Summa")
    def admin_total_amount(self, instance: Bill) -> str:
        total_amount = sum((x.amount for x in instance.expenses.all()), start=Decimal())
        return format_money(total_amount)
