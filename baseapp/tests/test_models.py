from django.test import TestCase
from baseapp.models import Product


class TestModels(TestCase):

    def test_models1(self):
        a = []
        for i in range(10):
            a.append(Product(id=i + 1, name='Товар ' + str(i + 1), price=1 * i ** 2 * 1000, amount=100 - i * 10))
            a[i].save()
            self.assertTrue(Product.objects.filter(id=a[i].id).exists(), f"data failure, id={a[i].id}")
        self.assertFalse(Product.objects.filter(id=999).exists(), f"id failure, result exists")
