import uuid

from django.db import models


class CheckList(models.Model):
    identifier = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField("namn", max_length=50)

    class Meta:
        verbose_name = "checklista"
        verbose_name_plural = "checklistor"

    def __str__(self) -> str:
        return self.name


class CheckListItem(models.Model):
    list = models.ForeignKey(CheckList, on_delete=models.CASCADE, related_name="items")
    description = models.CharField("beskrivning", max_length=100)

    class Meta:
        verbose_name = "punkt"
        verbose_name_plural = "punkter"

    def __str__(self) -> str:
        return self.description
