from django.conf import settings
from django.db import models


class Produto(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="produtos",
    )
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.nome} ({self.quantidade})"
