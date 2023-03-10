# Generated by Django 3.2.15 on 2023-01-17 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0060_alter_order_registered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodcartapp.restaurant', verbose_name='ресторан заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='зарегистрирован'),
        ),
    ]
