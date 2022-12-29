# Generated by Django 3.2.15 on 2022-12-29 19:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0059_alter_order_registered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2022, 12, 29, 19, 7, 2, 723613, tzinfo=utc), verbose_name='зарегистрирован'),
        ),
    ]
