from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Product, SingleOrder, Basket, User, PersonalDiscount


@registry.register_document
class ProductDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'products'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product
        fields = ['id',
                  'name',
                  'description',
                  'category',
                  'price',
                  'photo'
                  ]


@registry.register_document
class SingleOrderDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'singleorders'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = SingleOrder
        fields = ['sum_price',
                  ]


@registry.register_document
class BasketDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'baskets'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Basket
        fields = ['date',
                  'delivery_date',
                  'sum_price',
                  ]


@registry.register_document
class UserDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'users'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'is_active',
                  'is_admin',
                  'phone_number',
                  ]


@registry.register_document
class DiscountDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'discounts'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = PersonalDiscount
        fields = ['expires',
                  'name',
                  'value',
                  'amount',
                  ]
