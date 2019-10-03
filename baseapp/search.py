from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from operator import ior
from django.utils import six


def search(line, cat=None, sort_attr=None):
    client = Elasticsearch()
    if cat is None:
        s = Search(using=client, index="products")
        if line != '': s = s.query("match_phrase", name=line)
    else:
        queries = [Q('match', category=i) for i in cat]
        s = Search(using=client, index="products")
        if line != '':
             s = s.query(Q('match_phrase', name=line) &
                    Q(six.moves.reduce(ior, queries)))
        else:
             s = s.query(Q(six.moves.reduce(ior, queries)))
    response = s.execute()
    return sorted(response, key=lambda k: k['name' if sort_attr is None else sort_attr])


def query(i, line=None, attr=None, match_attr=None, sort_attr=None):
    client = Elasticsearch()
    s = Search(using=client, index=i)
    if line is not None:
        s = s.query("match_phrase" if match_attr is None else match_attr, \
                **{('name' if attr is None else attr): line})
    
    response = s.execute()
    return sorted(response, key=lambda k: \
        k[('name' if attr is None else attr) if sort_attr is None else sort_attr])
