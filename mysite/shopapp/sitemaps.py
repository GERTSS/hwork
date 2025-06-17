from django.contrib.sitemaps import Sitemap
from .models import Product

class ShopSitemap(Sitemap):
    changefreq = 'never'
    priority = 1

    def items(self):
        return Product.objects.filter(being_under_sanctions=False)

    def lastmod(self, item):
        return item.crated_by

