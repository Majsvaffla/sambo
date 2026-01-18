from __future__ import annotations

import htpy as h
from django.contrib import admin
from django.urls import reverse
from markupsafe import Markup

from sambo.admin import site

from .models import CheckList, CheckListItem


class ItemInline(admin.TabularInline[CheckListItem, CheckList]):
    model = CheckListItem
    fields = ["description"]
    extra = 0


@admin.register(CheckList, site=site)
class ListAdmin(admin.ModelAdmin[CheckList]):
    list_display = [
        "name",
        "admin_url",
        "admin_number_of_items",
    ]
    fields = ["name"]
    inlines = [ItemInline]

    @admin.display(description="URL")
    def admin_url(self, instance: CheckList) -> h.Element:
        return h.a(href=reverse("check_list", args=[instance.identifier]), target="_blank")[
            "Visa lista ", h.wa_icon(name="arrow-up-right-from-square")
        ]

    @admin.display(description="Antal punkter")
    def admin_number_of_items(self, instance: CheckList) -> str:
        return str(instance.items.count())
