from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from operator import ior
from django.utils import six


def search(line, cat=None, sort_attr=None):
    client = Elasticsearch()
    if cat is None:
        s = Search(using=client, index="products")\
            .query("match_phrase", name=line)\
            .sort('name' if sort_attr is None else sort_attr)
    else:
        queries = []
        for i in cat: queries.append(Q('match', category=i))
        s = Search(using=client, index="products")\
            .query(Q('match_phrase', name=line) & Q(six.moves.reduce(ior, queries)))\
            .sort('name' if sort_attr is None else sort_attr)
    response = s.execute()
    return [hit.name for hit in response]


print(search("Train", cat=['tech', 'food']))
