from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q


def search(line, cat = None):
    client = Elasticsearch()
    if cat == None: s = Search(using=client, index="products").query("match", name=line)
    else: s = Search(using=client, index="products").query(
        Q('match', name=line) & Q('contains', categories=cat))
    response = s.execute()

    return [hit.name for hit in response]


print(search("Train"))
