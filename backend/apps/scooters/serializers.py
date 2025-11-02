from rest_framework import serializers
from .models import ScooterModel, Scooter
from apps.cities.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "slug"]


class ScooterModelSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    available_scooters_count = serializers.ReadOnlyField()
    min_price = serializers.ReadOnlyField()

    class Meta:
        model = ScooterModel
        fields = [
            "id",
            "name",
            "slug",
            "city",
            "description",
            "available_scooters_count",
            "min_price",
        ]
        read_only_fields = ["slug"]


class ScooterSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source="model.name", read_only=True)
    city_name = serializers.CharField(source="model.city.name", read_only=True)
    city_slug = serializers.CharField(source="model.city.slug", read_only=True)

    class Meta:
        model = Scooter
        fields = [
            "slug",
            "model",
            "model_name",
            "city_name",
            "city_slug",
            "latitude",
            "longitude",
            "max_speed",
            "battery_level",
            "total_price",
            "is_available",
        ]
        read_only_fields = ["slug"]
