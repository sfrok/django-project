from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from operator import ior
from django.utils import six


def search(line, cat=None, sort_attr=None):
    client = Elasticsearch()
    if cat is None:
        if line != '':
            s = Search(using=client, index="products") \
                .query("match_phrase", name=line)  # \
                # .sort('name' if sort_attr is None else sort_attr)
        else:
            s = Search(using=client, index="products")
    else:
        queries = []
        for i in cat:
            queries.append(Q('match', category=i))
        if line != '':
            s = Search(using=client, index="products") \
                .query(Q('match_phrase', name=line) &
                    Q(six.moves.reduce(ior, queries)))
        else:
            s = Search(using=client, index="products") \
                .query(Q(six.moves.reduce(ior, queries)))
    response = s.execute()
    response = sorted(response, key=lambda k: k['name' if sort_attr is None else sort_attr])
    return [hit for hit in response]


def query(i, line=None, attr=None, match_attr=None, sort_attr=None):
    client = Elasticsearch()
    if line is not None:
        s = Search(using=client, index=i) \
            .query("match_phrase" if match_attr is None else match_attr, \
                **{('name' if attr is None else attr): line})  # \
            # .sort(('name' if attr is None else attr) if sort_attr is None else sort_attr)
    else:
        s = Search(using=client, index=i)
    
    response = s.execute()
    response = sorted(response, key=lambda k: \
        k[('name' if attr is None else attr) if sort_attr is None else sort_attr])
    return [vars(hit) for hit in response]


# print(search("", sort_attr='price'))
