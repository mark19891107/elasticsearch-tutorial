# coding=utf-8
import json
from pyes import ES,Search,MatchAllQuery
from tools.FileTools import FileTools
from tools.FormatTranslator import FormatTranslator
from pyes.aggs import TermsAgg
  
  
ftool = FileTools()
ftrans = FormatTranslator() 
  
# 1. Create Connection
conn = ES()
  
# 2. Index Data
dataset_json = open("../dataset.json")
dataset = json.load(dataset_json)['data']
for data in dataset:
    conn.index(data, "example_index", "example_type", "example_id_"+str(dataset.index(data)))
      
# 3. Create Simple Query
query = MatchAllQuery()
  
# 4. Create Simple Aggregation
agg = TermsAgg('agg1', field="name",sub_aggs=[],size=100)
  
# 5. Get Result
search = Search(query,size=5)
search.agg.add(agg)
print search.serialize()
  
result = conn.search(search, "example_index", "example_type" )
  
for i in result:
    print json.dumps(i,indent=2)
print json.dumps(result.aggs,indent=2)
  
result._do_search()
print json.dumps(result._results,indent=2)