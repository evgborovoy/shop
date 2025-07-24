from string import ascii_letters
from random import choices

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from shopapp.models import Product


class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.product_name = "".join(choices(ascii_letters, k=8))
        Product.objects.filter(name=self.product_name).delete()

    def test_product_create(self):
        response = self.client.post(
            reverse("shopapp:create_product"),
            {
                "name": self.product_name,
                "price": "179",
                "description": "New model of popular item",
                "discount": "5",
            })
        self.assertRedirects(response, reverse("shopapp:products_list"))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name="NewProduct")

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk}),
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk}),
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTest(TestCase):
    fixtures = [
        "products_fixture.json"
    ]

    def test_products(self):
        response = self.client.get(reverse("shopapp:products_list"))
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context["products"]),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, "shopapp/products_list.html")


class OrdersListViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="userTest", password="test_test")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:orders_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)
