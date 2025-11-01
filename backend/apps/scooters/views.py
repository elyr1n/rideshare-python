from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Count, Q
from django.contrib.auth.decorators import login_required

from .models import ScooterModel, Scooter
from apps.cities.models import City


@login_required()
def scooter_models_list(request):
    city_id = request.GET.get("city")
    scooter_models = ScooterModel.objects.all()

    if city_id:
        scooter_models = scooter_models.filter(city_id=city_id)

    scooter_models = scooter_models.annotate(
        min_price=Min("scooters__total_price"),
        available_count=Count("scooters", filter=Q(scooters__is_available=True)),
    )

    cities = City.objects.all()

    overall_min_price = min(
        (model.min_price for model in scooter_models if model.min_price), default=0
    )

    return render(
        request,
        "scooters/scooter_models_list.html",
        {
            "scooter_models": scooter_models,
            "min_price": overall_min_price,
            "cities": cities,
            "selected_city": city_id,
        },
    )


@login_required()
def scooter_list(request, model_slug):
    model = get_object_or_404(ScooterModel, slug=model_slug)
    scooters = Scooter.objects.filter(model=model, is_available=True)

    return render(
        request,
        "scooters/scooter_list.html",
        {
            "model": model,
            "scooters": scooters,
        },
    )


@login_required()
def scooter_detail(request, scooter_slug):
    scooter = get_object_or_404(Scooter, slug=scooter_slug, is_available=True)

    return render(
        request,
        "scooters/scooter_detail.html",
        {
            "scooter": scooter,
        },
    )
