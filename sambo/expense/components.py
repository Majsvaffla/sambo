from collections.abc import Iterable
from datetime import date

import htpy as h
from django.http import HttpRequest
from django.middleware import csrf
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


def expense(instance: Expense) -> h.Element:
    return h.tr(
        ".expense",
        {
            "@click": rf'location.href = "{reverse("expense_edit", args=[instance.bill.identifier, instance.pk])}"',
        },
    )[
        h.th(scope="row")[instance.description],
        h.td[instance.spent_at.isoformat()],
        h.td(".nowrap")[format_money(instance.amount)],
    ]


def expenses(instance: Bill, settled_at: date) -> Iterable[h.Element]:
    for i in instance.expenses.filter(settled_at__gt=settled_at).order_by("-spent_at"):
        yield expense(i)


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
                h.input(type="hidden", name="csrfmiddlewaretoken", value=csrf.get_token(request)),
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
    return h.wa_card("#bill")[
        h.h1(slot="header")[instance.name],
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
                unsettled_amount > 0
                and h.table[
                    h.caption["Ej uppgjorda utgifter"],
                    h.thead[
                        h.tr[
                            h.th(scope="col")["Beskrivning"],
                            h.th(scope="col")["Datum"],
                            h.th(scope="col", colspan=2)["Summa"],
                        ],
                    ],
                    h.tbody[expenses(instance, settled_at)],
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
            unsettled_amount > 0
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
