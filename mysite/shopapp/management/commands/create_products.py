from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Команда создания продуктов начала работу')
        Computer, created = Product.objects.get_or_create(name='HyperX', price=100000)
        Smartphone, created = Product.objects.get_or_create(name='iPhone', price=5500)
        self.stdout.write('Команда создания продуктов закончила работу')