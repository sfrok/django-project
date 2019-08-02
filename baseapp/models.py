from django.db import models

class Category(models.Model):
    def __init__(self, name='LOL'):
        self.name = name

class Product(models.Model):
    def __init__(self):
        self.name = 'LOL'
        self.desc = 'LOL MORE'
        self.cats = [Category() for i in range(5)]
        self.price = 0
        self.disc = []
        self.amount = 0
        self.sell_type = 0
        self.ship_to = []
        self.ship_prices = []
        self.photo = 'Image path here'
