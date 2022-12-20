# Generated by Django 3.2.15 on 2022-12-20 17:34

from django.db import migrations, models
import django.db.models.deletion
import foodcartapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20221220_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(verbose_name='количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[foodcartapp.models.validate_positive])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderproducts', to='foodcartapp.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderproducts', to='foodcartapp.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'элемент заказа',
                'verbose_name_plural': 'элементы заказа',
            },
        ),
        migrations.DeleteModel(
            name='OrderProducts',
        ),
    ]
