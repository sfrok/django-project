from elasticsearch import Elasticsearch
 
def search(line):
    es = Elasticsearch()
    res = es.search(index="СЕРЫЙ СКАЖИ ИМЯ", doc_type="products", body={"query": {"match": {"name": line}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['name']))