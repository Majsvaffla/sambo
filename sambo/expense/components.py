import json
from collections.abc import Iterable
from datetime import date

import htpy as h
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse

from sambo.components import page

from .formatters import format_money
from .models import Bill, Expense


def _page(request: HttpRequest, *content: h.Node, title: str) -> h.Element:
    return page(
        request,
        title=title,
        head=[
            h.link(rel="stylesheet", href=static("expense/styles.css")),
        ],
        main=content,
    )


def expense_row(instance: Expense, *, editable: bool, checkable: bool) -> h.Element:
    return h.tr(
        {
            "@click": rf'location.href = "{reverse("expense_edit", args=[instance.bill.identifier, instance.pk])}"',
        }
        if editable
        else {},
        class_=["expense", {"editable": editable}],
    )[
        h.th(scope="row")[instance.description],
        h.td[instance.spent_at.isoformat()],
        h.td(".nowrap")[format_money(instance.amount)],
        checkable
        and h.td[
            h.wa_checkbox(
                {
                    "@change": r"""
                        if ($event.target.checked) {
                            numberOfCheckedExpenses += 1
                        } else {
                            numberOfCheckedExpenses -= 1
                        }
                    """,
                },
                name="expenses",
                value=instance.pk,
                checked=True,
                size="large",
            )
        ],
    ]


def expense_rows(expenses: Iterable[Expense], *, editable: bool, checkable: bool) -> Iterable[h.Element]:
    for i in expenses:
        yield expense_row(i, editable=editable, checkable=checkable)


def expense_page(request: HttpRequest, instance: Expense) -> h.Element:
    return _page(
        request,
        h.wa_card[
            h.form[
                h.wa_input(
                    label="Beskrivning",
                    type="text",
                    name="description",
                    value=instance.description,
                    required=True,
                    maxlength=50,
                    autocomplete="off",
                    autofocus=True,
                ),
                h.wa_input(
                    label="Spenderad",
                    type="date",
                    name="spent_at",
                    value=instance.spent_at.isoformat(),
                    required=True,
                ),
                h.wa_input(
                    label="Summa",
                    type="number",
                    name="amount",
                    value=str(instance.amount),
                    required=True,
                    step="0.01",
                    min=0,
                )[h.span(slot="end")["kr"]],
                h.section(".actions")[
                    (
                        instance.pk
                        and h.wa_button(
                            variant="danger",
                            appearance="outlined",
                            hx_delete=reverse("expense_edit", args=[instance.bill.identifier, instance.pk]),
                            hx_disabled_elt="this",
                            hx_confirm=f"Är du säker på att du vill ta bort {instance.description}?",
                        )["Ta bort"]
                    ),
                    h.wa_button(
                        variant="success",
                        hx_post=(
                            reverse("expense_edit", args=[instance.bill.identifier, instance.pk])
                            if instance.pk
                            else reverse("expense_create", args=[instance.bill.identifier])
                        ),
                        hx_disabled_elt="this",
                    )["Spara"],
                ],
            ],
        ],
        title="Lägg till utgift",
    )


def bill(instance: Bill, settled_at: date) -> h.Element:
    unsettled_amount = instance.sum_unsettled_amount_at(settled_at)
    unsettled_expenses = instance.expenses.filter(settled_at__gt=settled_at).order_by("-spent_at")
    has_unsettled_expenses = len(unsettled_expenses) > 0

    return h.wa_card("#bill")[
        h.h1(slot="header")[instance.name],
        h.wa_dropdown(slot="header-actions")[
            h.wa_button(appearance="plain", slot="trigger")[h.wa_icon(name="gear", variant="solid", label="Hantera")],
            h.wa_dropdown_item[
                h.a(href=reverse("bill", args=[instance.identifier]) + "?action=copy")[
                    h.wa_icon(slot="icon", name="copy"), "Kopiera"
                ],
            ],
        ],
        h.section[
            h.wa_button(
                variant="brand",
                appearance="outlined",
                size="small",
                icon="plus",
                pill=True,
                href=reverse("expense_create", args=[instance.identifier]),
            )[
                h.wa_icon(slot="start", name="plus"),
                "Lägg till utgift",
            ],
            (
                has_unsettled_expenses
                and h.table[
                    h.caption["Ej uppgjorda utgifter"],
                    h.thead[
                        h.tr[
                            h.th(scope="col")["Beskrivning"],
                            h.th(scope="col")["Datum"],
                            h.th(scope="col", colspan=2)["Summa"],
                        ],
                    ],
                    h.tbody[expense_rows(unsettled_expenses, editable=True, checkable=False)],
                    h.tfoot[
                        h.tr[
                            h.th(scope="row", colspan=2)["Totalt"],
                            h.td[format_money(unsettled_amount)],
                        ],
                    ],
                ]
            ),
        ],
        (
            has_unsettled_expenses
            and h.section(slot="footer")[
                h.p[f"Att betala: {format_money(unsettled_amount / 2)}"],
                h.wa_button(
                    slot="footer-actions",
                    variant="brand",
                    hx_patch=reverse("bill", args=[instance.identifier]),
                    hx_confirm="Är du säker på att du vill göra upp om alla utgifter?",
                    hx_disabled_elt="this",
                )["Gör upp"],
            ]
        ),
    ]


def bill_page(request: HttpRequest, instance: Bill, settled_at: date) -> h.Element:
    return _page(
        request,
        bill(instance, settled_at),
        title=instance.name.capitalize(),
    )


def copy_page(request: HttpRequest, instance: Bill, spent_at: date) -> h.Element:
    settled_expenses = instance.expenses.filter(spent_at__gte=spent_at).order_by("-spent_at")
    rows = list(expense_rows(settled_expenses, editable=False, checkable=True))

    return _page(
        request,
        h.wa_card[
            h.wa_input(
                label="Utgifter sedan detta datum:",
                type="date",
                value=spent_at.isoformat(),
                autofocus=True,
                hx_get=reverse("bill", args=[instance.identifier]),
                hx_trigger="change",
                hx_vals=json.dumps({"action": "copy"}),
                hx_target="closest form",
                hx_select="form",
                hx_swap="outerHTML",
                hx_disabled_elt="this",
            ),
            h.form(x_data=f"{{numberOfCheckedExpenses: {len(rows)}}}")[
                h.table[rows] if rows else h.p["Det finns inga ej uppgjorda utgifter."],
                h.p[h.span(x_text="numberOfCheckedExpenses"), " utgifter kommer att kopieras."],
                h.section(".actions")[
                    h.wa_button(
                        variant="success",
                        disabled=not rows,
                        hx_post=reverse("bill", args=[instance.identifier]),
                        hx_vals=json.dumps({"action": "copy"}),
                        hx_disabled_elt="this",
                    )["Kopiera"],
                ],
            ],
        ],
        title="Kopiera utgifter",
    )
