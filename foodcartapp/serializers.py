from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer

from .models import Order
from .models import OrderProduct


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']



class OrderSerializer(ModelSerializer):
    products = OrderProductsSerializer(many=True, allow_empty=False, write_only=True)
    phonenumber = PhoneNumberField(region="RU")

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']
