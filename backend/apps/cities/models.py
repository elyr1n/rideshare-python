from django.db import models


class City(models.Model):
    name = models.CharField(max_length=25, verbose_name="Город")
    slug = models.SlugField(max_length=25, unique=True, verbose_name="URL")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name
