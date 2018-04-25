from dateutil import parser

def get_products(query):
    from elasticsearch import Elasticsearch
    es = Elasticsearch("http://es1.vgt.vito.be:9200")
    results = es.search(index="product_catalog_prod", body={"query":{
        "query_string" : {
            "query" : query,
            "use_dis_max" : True
        }
    }})

    hits = results['hits']['hits']
    products = [hit["_source"] for hit in hits]
    from string import Template
    cmd_template = Template("/data/CGS_S1_SLC_L1/IW/DV/$year/$month/$day/${title}/${title}.zip")
    for p in products:
        ingestion = parser.parse(p["properties"]["ingestiondate"])
        context = {
            "title":p["title"],
            "year":ingestion.year,
            "month":"%02d" % ingestion.month,
            "day":"%02d" % ingestion.day
        }
        p["local_filename"] =cmd_template.substitute(context)
    return products

#products = get_products("properties.beginposition:[2018-04-01 TO 2018-12-31] AND properties.orbitdirection:DESCENDING AND properties.platformname:Sentinel-1 AND properties.producttype:SLC AND properties.polarisationmode:\"VV VH\"")