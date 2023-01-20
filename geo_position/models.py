from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GeoPositionQuerySet(models.QuerySet):
    def coordinates(self, address):
        return self.filter(address=address)\
                   .values_list("longitude", "latitude")


class GeoPosition(models.Model):
    address = models.CharField(
        verbose_name="адрес",
        max_length=100,
        blank=True,
        unique=True
    )

    longitude = models.FloatField(
        verbose_name="долгота",
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
    )
    latitude = models.FloatField(
        verbose_name="широта",
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )

    objects = GeoPositionQuerySet.as_manager()

    class Meta:
        verbose_name = "гео позиция"
        verbose_name_plural = "гео позиции"
