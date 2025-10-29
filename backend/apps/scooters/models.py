from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Scooter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    max_speed = models.IntegerField()
    battery_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    total_price = models.IntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Scooter"
        verbose_name_plural = "Scooters"

    def __str__(self):
        return f"{self.name}"
