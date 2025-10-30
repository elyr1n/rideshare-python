from django.db import models


class City(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=25, unique=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name
