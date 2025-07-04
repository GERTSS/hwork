from django.contrib.auth.models import User
from django.db import models
from django.template.base import kwarg_re
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy

from myauth.models import Profile

class Product(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=20, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(null=False, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    being_under_sanctions = models.BooleanField(default=False)
    crated_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')

    def get_absolute_url(self):
        return reverse_lazy('shopapp:product_details', kwargs={'pk': self.pk})


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    address = models.TextField(null=False)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_archived = models.BooleanField(default=False)
    products = models.ManyToManyField(Product, related_name='orders')
