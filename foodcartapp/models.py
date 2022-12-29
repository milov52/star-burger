from django.utils import timezone

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q, Sum
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def available(self):
        orders = (
            Order.objects
            .filter(~Q(status='F'))
            .order_by('id')
        )
        return orders.annotate(
            order_amount=Sum(F('orderproducts__quantity') * F('orderproducts__price'))
        )

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('new', 'Необработанный'),
        ('make', 'Изготавливается'),
        ('assembled', 'Собран'),
        ('delievery', 'В доставке'),
        ('finish', 'Выполнен'),
    ]

    ORDER_PAYMENT_METHODS = [
        ('cash', 'Наличными'),
        ('electron', 'Электронно')
    ]

    firstname = models.CharField(
        'имя',
        max_length=20)
    lastname = models.CharField(
        'фамилия',
        max_length=20,
        db_index=True)
    address = models.CharField(
        'адрес',
        max_length=100)
    phonenumber = PhoneNumberField(
        'мобильный телефон',
        region='RU'
    )
    status = models.CharField(
        'статус заказа',
        choices=ORDER_STATUS_CHOICES,
        default='new',
        db_index=True,
        max_length=10
    )
    comments = models.TextField(
        'комментарий',
        blank=True
    )

    payment_method = models.CharField(
        'cпособ оплаты',
        choices=ORDER_PAYMENT_METHODS,
        default='cash',
        max_length=10,
        db_index=True
    )

    registered_at = models.DateTimeField(
        'зарегистрирован',
        default=timezone.now(),
        db_index=True
    )

    called_at = models.DateTimeField('совершен звонок', blank=True, null=True)
    dellivired_at = models.DateTimeField('доставлен', db_index=True, blank=True, null=True)

    order_restaurant = models.ForeignKey(Restaurant,
                                    on_delete=models.CASCADE,
                                    verbose_name='ресторан',
                                    blank=True,
                                    null=True)


    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.address}"


def validate_positive(price):
    if price < 0:
        raise ValidationError('Стоимость должна быть положительной')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='order_products',
                              verbose_name='заказ'
                              )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='order_products',
                                verbose_name='продукт')
    quantity = models.SmallIntegerField('количество',
                                        validators=[MinValueValidator(1)])
    price = models.DecimalField('цена',
                                max_digits=5,
                                decimal_places=2,
                                validators=[validate_positive]
                                )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f"{self.product.name} {self.order.firstname} {self.order.lastname}"
