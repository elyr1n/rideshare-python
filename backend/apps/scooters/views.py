from django.shortcuts import render
from .models import Scooter
from apps.cities.models import City


def scooter_list(request):
    city_id = request.GET.get("city")

    scooters = Scooter.objects.all()
    available_scooters = Scooter.objects.available_scooters()

    if city_id:
        scooters = scooters.filter(city_id=city_id)
        available_scooters = available_scooters.filter(city_id=city_id)

    min_price = Scooter.objects.get_min_price()
    cities = City.objects.all()

    return render(
        request,
        "scooters/scooter_list.html",
        {
            "scooters": scooters,
            "available_scooters": available_scooters,
            "min_price": min_price,
            "cities": cities,
            "selected_city": city_id,
        },
    )


def scooter_detail(request, slug):
    scooter = Scooter.objects.get(slug=slug)
    return render(request, "scooters/scooter_detail.html", {"scooter": scooter})
