from django.core.management import BaseCommand
from shopapp.models import Product
from myauth.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Команда создания продуктов начала работу')
        profile = Profile.objects.first()
        Computer, created = Product.objects.get_or_create(name='HyperX', price=100000, crated_by=profile)
        Smartphone, created = Product.objects.get_or_create(name='iPhone', price=5500, crated_by=profile)
        self.stdout.write('Команда создания продуктов закончила работу')