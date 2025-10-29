from django.db import models


class Rental(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    scooter = models.ForeignKey("scooters.Scooter", on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Rental"
        verbose_name_plural = "Rentals"

    def __str__(self):
        return f"{self.user} | {self.scooter} | {self.total_price}"
