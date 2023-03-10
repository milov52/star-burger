# Generated by Django 3.2.15 on 2022-12-20 20:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_auto_20221220_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='called_at',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='dellivired_at',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='registered_at',
        ),
        migrations.AddField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='совершен звонок'),
        ),
        migrations.AddField(
            model_name='order',
            name='dellivired_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='доставлен'),
        ),
        migrations.AddField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2022, 12, 20, 20, 48, 48, 100176, tzinfo=utc), verbose_name='зарегистрирован'),
        ),
    ]
