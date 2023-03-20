from django.db import models

from backend.models.TimeBasedModel import TimeBasedModel


class Role(TimeBasedModel):
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    name = models.CharField("Роль", max_length=255, unique=True)

    def __str__(self):
        return self.name
