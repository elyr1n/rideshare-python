import shortuuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Min


class ScooterManager(models.Manager):
    def available_scooters(self):
        return self.filter(is_available=True)

    def get_min_price(self):
        return self.aggregate(min_price=Min("total_price"))["min_price"] or 0


class ScooterModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    city = models.ForeignKey("cities.City", on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        verbose_name = "Scooter Model"
        verbose_name_plural = "Scooter Models"

    def __str__(self):
        return f"{self.name}"

    def available_scooters_count(self):
        return self.scooters.filter(is_available=True).count()

    def get_min_price(self):
        result = self.scooters.filter(is_available=True).aggregate(
            min_price=Min("total_price")
        )
        return result["min_price"] or 0


class Scooter(models.Model):
    slug = models.CharField(max_length=100, unique=True, default=shortuuid.uuid)
    model = models.ForeignKey(
        "scooters.ScooterModel", on_delete=models.CASCADE, related_name="scooters"
    )
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
        return f"{self.slug}"
