from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Min


class ScooterManager(models.Manager):
    def available_scooters(self):
        return self.filter(is_available=True)

    def get_min_price(self):
        return self.aggregate(min_price=Min("total_price"))["min_price"] or 0


class Scooter(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    city = models.ForeignKey("cities.City", on_delete=models.CASCADE)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    max_speed = models.IntegerField()
    battery_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    total_price = models.IntegerField()
    is_available = models.BooleanField(default=True)

    objects = ScooterManager()

    class Meta:
        verbose_name = "Scooter"
        verbose_name_plural = "Scooters"

    def __str__(self):
        return f"{self.name}"
