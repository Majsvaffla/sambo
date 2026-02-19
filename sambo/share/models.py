import uuid

from django.db import models


class Upload(models.Model):
    identifier = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    content = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "uppladdning"
        verbose_name_plural = "uppladdningar"

    def __str__(self) -> str:
        return self.name
