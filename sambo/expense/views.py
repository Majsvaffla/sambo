from datetime import date
from uuid import UUID
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from . import components
from .forms import ExpenseForm
from .models import Bill, Expense


def bill(request: HttpRequest, bill_identifier: UUID, settled_at: date = date.max) -> HttpResponse:
    today = timezone.now().date()
    if settled_at == date.max:
        return redirect("bill_settled_at", bill_identifier, today)

    bill_instance = get_object_or_404(Bill.objects, identifier=bill_identifier)

    if request.method == "GET":
        return HttpResponse(components.bill(request, bill_instance, settled_at))

    if request.method == "POST":
        if (form := ExpenseForm(request.POST or None)).is_valid():
            expense_instance = form.save(commit=False)
            expense_instance.bill = bill_instance
            expense_instance.save()
            return HttpResponse(components.expense(expense_instance))
        return HttpResponse(status=400)

    if request.method == "PATCH":
        bill_instance.expenses.filter(settled_at__gte=today).update(settled_at=today)
        return HttpResponse(components.bill(request, bill_instance, settled_at))

    return HttpResponse(status=405)




def expense(request: HttpRequest, bill_identifier: UUID, expense_pk: int | None = None) -> HttpResponse:
    if request.method == "GET":
        bill_instance = get_object_or_404(Bill.objects, identifier=bill_identifier)
        form = ExpenseForm()
        return HttpResponse(components.expense_form(bill_instance))

    expense_instance = get_object_or_404(Expense.objects, pk=expense_pk, bill__identifier=bill_identifier)

    if request.method == "DELETE":
        expense_instance.delete()
        return HttpResponse(components.expenses(expense_instance.bill))

    if request.method == "POST":
        if (form := ExpenseForm(request.POST or None, instance=expense_instance)).is_valid():
            expense_instance = form.save()
            return HttpResponse(components.expense(expense_instance))
        return HttpResponse(status=400)

    return HttpResponse(status=405)
