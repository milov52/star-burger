# Generated by Django 3.2.15 on 2022-12-20 20:06

from django.db import migrations, models
import foodcartapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_auto_20221220_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('N', 'Необработанный'), ('С', 'Согласован с клиентом'), ('A', 'Собран'), ('D', 'В доставке'), ('F', 'Выполнен')], db_index=True, default='N', max_length=2, verbose_name='статус заказа'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[foodcartapp.models.validate_positive_price], verbose_name='цена'),
        ),
    ]
