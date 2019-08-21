from django_elasticsearch_dsl import DocType, Index
from baseapp.models import Product
from elasticsearch_dsl.connections import connections

connections.create_connection()
prod = Index('products') 
prod.settings( number_of_shards=1, number_of_replicas=0)
@prod.doc_type
class ProductDoc(DocType):
    class Meta:
        model = Product
        fields = ['name',
    'description',
    'categories',
    'price',
    'discount',
    'amount',
    'selling_type',
    'ship_to',
    'ship_price',
    'ship_discount',
    'photo',
    'post_date']