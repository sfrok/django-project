from django.test import TestCase

import baseapp.scripts as func
from baseapp.models import Product, Category


class TestDB(TestCase):
    @classmethod
    def setUpTestData(cls):
        # DO NOT MODIFY THIS DATA OUTSIDE SETUP!
        cls.data = []
        for i in range(10):
            cls.data.append(Product(
                id=i + 1,
                name='Товар ' + str(i + 1),
                description='Это описание товара №' + str(i + 1) + '.',
                amount=100 - i * 5,
                price=(i + 1) ** 2 * 1000 - 1000 * i))

    def test_model_product(self):
        for i in self.data:
            i.save()
            self.assertTrue(Product.objects.filter(id=i.id).exists(), f"data failure, id={i.id}")
        self.assertFalse(Product.objects.filter(id=999).exists(), f"id failure, result exists")

    def test_search_line(self):
        f = func.search('Товар 3')
        self.assertTrue(f[0]['name'] == 'Товар 3', 
                        f"results aren't equal:\nES: {f}\n f[0]['name']: {f[0]['name']}")
