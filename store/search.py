from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
 
def search(line):
    client = Elasticsearch()
    s = Search(using=client, index="products").query("match", title=line)
    response = s.execute()

    for hit in response:
        print(hit.meta.score, hit.title)
    for tag in response.aggregations.per_tag.buckets:
        print(tag.key, tag.max_lines.value)