from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField


from .models import OrderProducts
from .models import Order

class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderProductsSerializer(many=True)
    phonenumber = PhoneNumberField(region="RU")

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']

    def validate_products(self, products):
        if not products:
            raise ValidationError('Этот список не может быть пустым')
        return products
