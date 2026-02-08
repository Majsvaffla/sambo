from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from dateutil.relativedelta import relativedelta
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone

from . import components
from .forms import ExpenseForm
from .models import Bill, Expense

if TYPE_CHECKING:
    from uuid import UUID


def _today() -> date:
    return timezone.now().date()


def _hx_redirect_to_bill(bill_identifier: UUID) -> HttpResponse:
    return HttpResponse(headers={"HX-Redirect": reverse("bill", args=[bill_identifier])})


def bill(request: HttpRequest, bill_identifier: UUID | None = None) -> HttpResponse:
    bill_instance = get_object_or_404(Bill.objects, identifier=bill_identifier) if bill_identifier else Bill()
    today = _today()

    if request.method == "GET":
        if request.GET.get("action") == "copy":
            if "spent_at" in request.GET:
                spent_at = date.fromisoformat(request.GET["spent_at"])
            else:
                last_month = today - relativedelta(months=1)
                spent_at = date(last_month.year, last_month.month, 1)

            return HttpResponse(components.copy_page(request, bill_instance, spent_at))

        return HttpResponse(components.bill_page(request, bill_instance, today))

    if request.method == "POST":
        if bill_identifier is None:
            if "name" not in request.POST:
                return HttpResponse(status=400)

            if request.POST.get("hxneypxtz") != "yum":
                return HttpResponse(status=400)

            assert bill_instance.pk is None
            bill_instance.name = request.POST["name"]
            bill_instance.save()
            return _hx_redirect_to_bill(bill_instance.identifier)

        if "action" not in request.POST or "expenses" not in request.POST:
            return HttpResponse(status=400)

        assert request.POST["action"] == "copy"

        bill_instance.expenses.bulk_create(
            Expense(description=expense.description, amount=0, bill=bill_instance)
            for expense in bill_instance.expenses.filter(pk__in=(int(x) for x in request.POST.getlist("expenses")))
        )
        return _hx_redirect_to_bill(bill_identifier)

    if request.method == "PATCH":
        if bill_identifier is None:
            return HttpResponse(status=400)

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
