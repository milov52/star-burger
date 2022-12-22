# Generated by Django 3.2.15 on 2022-12-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo_position', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geoposition',
            name='type',
            field=models.CharField(choices=[('R', 'Ресторан'), ('R', 'Заказ')], default='O', max_length=2, verbose_name='тип адреса'),
        ),
    ]