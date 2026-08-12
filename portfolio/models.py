from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Skill(models.Model):
    """Tallentaa yhden CV-sivustolla näytettävän taidon."""

    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name
