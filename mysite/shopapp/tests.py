from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from django.contrib.contenttypes.models import ContentType
from shopapp.models import Order
from django.urls import reverse
import logging

logger = logging.getLogger('shoapapp')


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='babyjhon', password='1234')
        cls.order = Order.objects.create(address='Main 12123', promocode='1234', user=cls.user)
        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.get(codename='view_order', content_type=content_type)
        cls.user.user_permissions.add(permission)

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.user.delete()

    def test_order_view(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, 'Main 12123')
        self.assertContains(response, '1234')
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    fixtures = ['users.json', 'products.json', 'orders.json']

    def setUp(self):
        self.user = User.objects.create_user(username='babyjhon', password='1234', is_staff=True)
        self.client.force_login(self.user)

    def tearDown(self):
        self.user.delete()

    def test_get_list_orders(self):
        response = self.client.get(reverse('shopapp:orders_get_copy'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data['orders']) == 3)
        order = data['orders'][0]
        self.assertEqual(order['id'], 1)
        self.assertEqual(order['address'], "Main Street 1")
        self.assertEqual(order['promocode'], '')
        self.assertEqual(order['products'], [1, 2, 3, 4])
        self.assertEqual(order['user'], 1)


