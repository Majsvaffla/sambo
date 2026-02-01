from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from . import components
from .forms import ExpenseForm
from .models import Bill, Expense

if TYPE_CHECKING:
    from datetime import date
    from uuid import UUID


def _today() -> date:
    return timezone.now().date()


def _hx_redirect_to_bill(bill_identifier: UUID) -> HttpResponse:
    return HttpResponse(headers={"HX-Redirect": reverse("bill", args=[bill_identifier])})


def bill(request: HttpRequest, bill_identifier: UUID) -> HttpResponse:
    bill_instance = get_object_or_404(Bill.objects, identifier=bill_identifier)

    if request.method == "GET":
        return HttpResponse(components.bill_page(request, bill_instance, _today()))

    if request.method == "PATCH":
        today = _today()
        bill_instance.expenses.filter(settled_at__gte=today).update(settled_at=today)
        return _hx_redirect_to_bill(bill_identifier)

    return HttpResponse(status=405)


def expense(request: HttpRequest, bill_identifier: UUID, expense_pk: int | None = None) -> HttpResponse:
    bill_instance = get_object_or_404(Bill.objects, identifier=bill_identifier)
    expense_instance = (
        get_object_or_404(bill_instance.expenses, pk=expense_pk) if expense_pk else Expense(bill=bill_instance)
    )

    if request.method == "GET":
        return HttpResponse(components.expense_page(request, expense_instance))

    if request.method == "DELETE":
        if not expense_instance.pk:
            return HttpResponse(status=400)

        expense_instance.delete()

        return _hx_redirect_to_bill(bill_identifier)

    if request.method == "POST":
        form = ExpenseForm(request.POST or None, instance=expense_instance)
        if form.is_valid():
            form.save()
            return _hx_redirect_to_bill(bill_identifier)

        return HttpResponse(status=400)

    return HttpResponse(status=405)
