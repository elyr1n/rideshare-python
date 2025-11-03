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
    name = models.CharField(max_length=100, verbose_name="Модель")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    city = models.ForeignKey(
        "cities.City", on_delete=models.CASCADE, verbose_name="Город"
    )
    description = models.CharField(max_length=150, verbose_name="Описание")

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"

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
    image = models.ImageField(upload_to="scooters", verbose_name="Фото")
    slug = models.CharField(
        max_length=100, unique=True, default=shortuuid.uuid, verbose_name="URL"
    )
    model = models.ForeignKey(
        "scooters.ScooterModel",
        on_delete=models.CASCADE,
        related_name="scooters",
        verbose_name="Модель",
    )
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    max_speed = models.IntegerField(verbose_name="Максимальная скорость")
    battery_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Уровень батареи",
    )
    total_price = models.IntegerField(verbose_name="Общая стоимость")
    is_available = models.BooleanField(default=True, verbose_name="Доступность")

    objects = ScooterManager()

    class Meta:
        verbose_name = "Самокат"
        verbose_name_plural = "Самокаты"

    def __str__(self):
        return f"{self.model.name} ({self.slug})"
