from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Scooter(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    battery_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_available = models.BooleanField()

    class Meta:
        verbose_name = "Scooter"
        verbose_name_plural = "Scooters"

    def __str__(self):
        return f"{self.name} | {self.id}"
