import uuid
from datetime import date

from django.db import models
from django.utils import timezone


def _today() -> date:
    return timezone.now().date()


class Bill(models.Model):
    identifier = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField("namn", max_length=50)

    class Meta:
        verbose_name = "nota"
        verbose_name_plural = "notor"

    def __str__(self) -> str:
        return self.name


class Expense(models.Model):
    description = models.CharField("beskrivning", max_length=50)
    amount = models.DecimalField("summa", max_digits=7, decimal_places=2)
    spent_at = models.DateField("spenderad", default=_today)
    spent_by = models.CharField("spenderad av", blank=True)
    settled_at = models.DateField("uppgjord", default=date.max, blank=True)

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="expenses")

    class Meta:
        verbose_name = "utgift"
        verbose_name_plural = "utgifter"

    def __str__(self) -> str:
        return self.description
