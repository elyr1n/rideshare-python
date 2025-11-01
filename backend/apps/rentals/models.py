from django.db import models


class Rental(models.Model):
    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    scooter = models.ForeignKey(
        "scooters.Scooter", on_delete=models.CASCADE, verbose_name="Самокат"
    )
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Время аренды")
    end_time = models.DateTimeField(
        null=True, blank=True, verbose_name="Время возврата"
    )

    class Meta:
        verbose_name = "Арендатор"
        verbose_name_plural = "Арендаторы"

    def __str__(self):
        return f"{self.user} | {self.scooter}"
