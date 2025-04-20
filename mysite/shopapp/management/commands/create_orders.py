from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from myauth.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Команда создания заказов начала работу')
        user = User.objects.filter(username="admin").first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='admin')
            Profile.objects.create(user=user)
        products = Product.objects.all()
        order1, created = Order.objects.get_or_create(address='Main Street 1', user=user)
        for product in products:
            order1.products.add(product)
        self.stdout.write('Команда создания заказов закончила работу')