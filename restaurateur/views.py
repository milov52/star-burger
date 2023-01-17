import requests
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from geopy import distance

from foodcartapp.models import Order, Product, Restaurant
from geo_position.models import GeoPosition


class Login(forms.Form):
    username = forms.CharField(
        label="Логин",
        max_length=75,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Укажите имя пользователя"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        max_length=75,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={"form": form})

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(
            request,
            "login.html",
            context={
                "form": form,
                "ivalid": True,
            },
        )


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("restaurateur:login")


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_products(request):
    restaurants = list(Restaurant.objects.order_by("name"))
    products = list(Product.objects.prefetch_related("menu_items"))

    products_with_restaurant_availability = []
    for product in products:
        availability = {
            item.restaurant_id: item.availability for item in product.menu_items.all()
        }
        ordered_availability = [
            availability.get(restaurant.id, False) for restaurant in restaurants
        ]

        products_with_restaurant_availability.append((product, ordered_availability))

    return render(
        request,
        template_name="products_list.html",
        context={
            "products_with_restaurant_availability": products_with_restaurant_availability,
            "restaurants": restaurants,
        },
    )


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_restaurants(request):
    return render(
        request,
        template_name="restaurants_list.html",
        context={
            "restaurants": Restaurant.objects.all(),
        },
    )


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

def get_suitable_restaurants(order, all_restaurant):
    order_product_list = [item.product.id for item in order.items.all()]

@user_passes_test(is_manager, login_url="restaurateur:login")
def view_orders(request):
    order_items = Order.objects.unfinished().annotate(
            order_amount=Sum(F('order_products__quantity') * F('order_products__price'))
        )

    restaurants = Restaurant.objects.all()
    restaurant_coordinates = []
    for restaurant in restaurants:
        restaurant_coordinates = {restaurant.id : GeoPosition.objects.coordinates(
            address=restaurant.address)}

    order_with_restaurants = []
    for order in order_items:
        available_restaurants = set()

        products = [
            order_products.product for order_products in order.order_products.all()
        ]

        for product in products:

            availability = [
                item.restaurant
                for item in product.menu_items.all()
                if item.availability
            ]
            if not available_restaurants:
                available_restaurants = set(availability)
            else:
                available_restaurants = available_restaurants & set(availability)

        order_coordinates = GeoPosition.objects.coordinates(address=order.address)
        restaurants_with_distance = {}
        for restaurant in available_restaurants:
            if restaurant.id in restaurant_coordinates.keys():
                restaurants_with_distance[restaurant] = round(
                    distance.distance(order_coordinates, restaurant_coordinates[restaurant.id]).km, 3
            )

        restaurants_with_distance = dict(
            sorted(restaurants_with_distance.items(), key=lambda item: item[1])
        )
        order_with_restaurants.append((order, restaurants_with_distance))

    return render(
        request,
        template_name="order_items.html",
        context={
            "order_items": order_with_restaurants,
        },
    )
