# Generated by Django 3.2.15 on 2022-12-19 20:15

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_auto_20221219_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(default="123", max_length=128, region='RU', verbose_name='мобильный телефон'),
            preserve_default=False,
        ),
    ]