# Generated by Django 3.2.15 on 2022-12-29 15:03

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_auto_20221223_2016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='restaurant',
            new_name='order_restaurant',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличными'), ('electron', 'Электронно')], db_index=True, max_length=10, verbose_name='cпособ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2022, 12, 29, 15, 3, 46, 80759, tzinfo=utc), verbose_name='зарегистрирован'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='foodcartapp.order', verbose_name='заказ'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='foodcartapp.product', verbose_name='продукт'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество'),
        ),
    ]
