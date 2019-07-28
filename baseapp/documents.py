from elasticsearch_dsl.connections import connections
# Create a connection to ElasticSearch
connections.create_connection()

from django_elasticsearch_dsl import DocType, Index
from .models import Book

book = Index('books') 

# reference elasticsearch doc for default settings here
book.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@book.doc_type
class BookDocument(DocType):

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'category']

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
client = Elasticsearch()
my_search = Search(using=client)

# define simple search here
# Simple search function
def search(title):
    query = my_search.query("match", title=title)
    response = query.execute()
    return response