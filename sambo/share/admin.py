from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.contrib import admin
from django.utils.formats import number_format

from sambo.admin import site
from sambo.components import details_url

from .models import Upload

if TYPE_CHECKING:
    import htpy as h


@admin.register(Upload, site=site)
class UploadAdmin(admin.ModelAdmin[Upload]):
    list_display = [
        "name",
        "admin_size",
        "admin_url",
        # "uploaded_at",
    ]
    fields = ["name"]

    @admin.display(description="Storlek (MB)")
    def admin_size(self, instance: Upload) -> str:
        content_megabytes = Decimal(len(instance.content)) / 1_000_000
        return number_format(
            content_megabytes,
            decimal_pos=0 if content_megabytes % 1 == 0 else 2,
            force_grouping=True,
        )

    @admin.display(description="URL")
    def admin_url(self, instance: Upload) -> h.Element:
        return details_url(instance, title="Visa uppladdning", url_pattern_name="uploaded")
