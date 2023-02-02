import requests
from django.conf import settings

from geo_position.models import GeoPosition


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat



def add_geoposition(address):
    if GeoPosition.objects.filter(address=address):
        return None

    coordinates = fetch_coordinates(settings.API_YANDEX_GEO_KEY, address)
    if not coordinates:
        return None

    longitude, latitude = coordinates

    GeoPosition.objects.create(
        address=address, longitude=longitude, latitude=latitude
    )
