from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def search(line):
    client = Elasticsearch()
    s = Search(using=client, index="products").query("match", name=line)
    response = s.execute()

    return [hit.name for hit in response]


print(search("Train"))
