from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Min, Q

from .models import ScooterModel, Scooter
from apps.cities.models import City
from .serializers import ScooterModelSerializer, ScooterSerializer, CitySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = "slug"


class ScooterModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScooterModel.objects.all()
    serializer_class = ScooterModelSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["city", "city__slug"]
    search_fields = ["name", "description", "city__name"]
    ordering_fields = ["name", "min_price"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = ScooterModel.objects.select_related("city").annotate(
            available_scooters_count=Count(
                "scooters", filter=Q(scooters__is_available=True)
            ),
            min_price=Min("scooters__total_price"),
        )
        return queryset

    @action(detail=True, methods=["get"])
    def scooters(self, request, slug=None):
        model = self.get_object()
        scooters = Scooter.objects.filter(model=model).select_related(
            "model", "model__city"
        )
        serializer = ScooterSerializer(scooters, many=True)
        return Response(serializer.data)


class ScooterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["model", "model__city", "model__city__slug", "is_available"]
    search_fields = ["model__name", "model__city__name"]
    ordering_fields = ["max_speed", "battery_level", "total_price"]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Scooter.objects.select_related("model", "model__city")

        min_battery = self.request.query_params.get("min_battery")
        if min_battery:
            queryset = queryset.filter(battery_level__gte=min_battery)

        min_speed = self.request.query_params.get("min_speed")
        if min_speed:
            queryset = queryset.filter(max_speed__gte=min_speed)

        return queryset

    @action(detail=False, methods=["get"])
    def available(self, request):
        available_scooters = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(available_scooters, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_city(self, request, city_slug=None):
        scooters = self.get_queryset().filter(model__city__slug=city_slug)
        serializer = self.get_serializer(scooters, many=True)
        return Response(serializer.data)
