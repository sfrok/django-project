from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Product, Order, Status, User, PersonalDiscount


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
        fields = ['name',
                  'description',
                  'category',
                  'price',
                  'photo'
                  ]


@registry.register_document
class OrderDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'orders'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Order
        fields = ['date',
                  'delivery_date',
                  'sum_price',
                  'sum_ship_price',
                  ]


@registry.register_document
class StatusDoc(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'statuses'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Status
        fields = ['name',
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
                  'a_country',
                  'a_city',
                  'a_address',
                  'post_index',
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
