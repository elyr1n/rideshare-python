from django.shortcuts import render
from .models import Scooter
from django.db.models import Min


def scooter_list(request):
    scooters = Scooter.objects.all()
    available_scooters = [s for s in scooters if s.is_available]
    min_price = scooters.aggregate(Min("total_price"))["total_price__min"]

    return render(
        request,
        "scooters/scooter_list.html",
        {
            "scooters": scooters,
            "available_scooters": available_scooters,
            "min_price": min_price,
        },
    )
