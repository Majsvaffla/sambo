from __future__ import annotations

import typing as t

from django.contrib import admin, messages

from .models import User

if t.TYPE_CHECKING:
    from django import forms
    from django.db.models.query import QuerySet
    from django.http import HttpRequest


class SamboAdminSite(admin.AdminSite):
    site_header = "sambo.tordavid.xyz"
    site_title = site_header
    index_title = "Administration"
    site_url = None
    enable_nav_sidebar = False


site = SamboAdminSite(name="sambo")


@admin.action(description="Generera nytt lösenord")
def set_random_password(modeladmin: UserAdmin, request: HttpRequest, queryset: QuerySet[User]) -> None:
    try:
        user = queryset.get()
        password = user.set_random_password()
        user.save()
        messages.info(request, f"Nytt lösenord: {password}")

    except (User.DoesNotExist, User.MultipleObjectsReturned):
        messages.warning(request, "Välj exakt en användare att återställa lösenordet för.")


@admin.register(User, site=site)
class UserAdmin(admin.ModelAdmin[User]):
    readonly_fields = ["last_login"]

    exclude = ["password"]
    actions = [set_random_password]

    def save_model(self, request: HttpRequest, obj: User, form: forms.Form, change: bool) -> None:
        password = obj.set_random_password()
        messages.info(request, f"Lösenord: {password}")

        super().save_model(request=request, obj=obj, form=form, change=change)
