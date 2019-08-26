from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from operator import ior
from django import utils




def search(line, cat = None):
    client = Elasticsearch()
    
    if cat == None: s = Search(using=client, index="products").query("match_phrase", name=line)
    else:
        queries = []
        for i in cat: queries.append(Q('match', category=i))
        s = Search(using=client, index="products").query(
        Q('match_phrase', name=line) & Q(utils.six.moves.reduce(ior, queries)))
    response = s.execute()

    return [hit.name for hit in response]


print(search("Train"))
