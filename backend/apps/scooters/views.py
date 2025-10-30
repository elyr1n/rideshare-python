from django.shortcuts import render
from .models import Scooter


def scooter_list(request):
    scooters = Scooter.objects.all()
    available_scooters = Scooter.objects.available_scooters()
    min_price = Scooter.objects.get_min_price()

    return render(
        request,
        "scooters/scooter_list.html",
        {
            "scooters": scooters,
            "available_scooters": available_scooters,
            "min_price": min_price,
        },
    )


def scooter_detail(request, slug):
    scooter = Scooter.objects.get(slug=slug)
    return render(request, "scooters/scooter_detail.html", {"scooter": scooter})
