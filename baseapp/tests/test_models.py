from django.test import TestCase
from baseapp.models import Product
import baseapp.search as func


class TestDB(TestCase):
    @classmethod
    def setUpTestData(cls):
        # DO NOT MODIFY THIS DATA OUTSIDE SETUP!
        cls.data = []
        for i in range(10):
            cls.data.append(Product(
                id=i + 1,
                name='Товар ' + str(i + 1),
                price=i ** 2 * 1000,
                amount=100 - i * 10))

    def test_model_product(self):
        for i in self.data:
            i.save()
            self.assertTrue(Product.objects.filter(id=i.id).exists(), f"data failure, id={i.id}")
        self.assertFalse(Product.objects.filter(id=999).exists(), f"id failure, result exists")

    def test_search_line(self):
        f = func.search('Товар 3')
        self.assertTrue(f[0]['name'] == 'Товар 3', 
                        f"results aren't equal:\nES: {f}\n f[0]['name']: {f[0]['name']}")
