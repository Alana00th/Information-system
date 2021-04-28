from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "\"%s\"" % (self.name)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class Invent(models.Model):
    stuff = models.CharField(max_length=128)
    shop = models.ForeignKey(Shop, blank=False, null=False, default=None, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентарь'