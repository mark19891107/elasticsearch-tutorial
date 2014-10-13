#coding=utf-8
import pyes
import json
import FormatTranslator
import FileTools

'''------------------------------------------- Matrix to csv -------------------------------------------'''

conn=pyes.es.ES('localhost:9200')
q = pyes.MatchAllQuery()
tagg = pyes.aggs.TermsAgg('user_id', field= 'user_id', sub_aggs=[]) 
tagg1 = pyes.aggs.TermsAgg('name', field= 'name')  
tagg.sub_aggs.append(tagg1) 
qsearch = pyes.query.Search(q) 
qsearch.agg.add(tagg)
 
rs = conn.search(query=qsearch , indices='example_index' ,type="example_type" )
print json.dumps(rs.aggs,indent=2)
 
formatTranslator = FormatTranslator.FormatTranslator()
result = formatTranslator.ES_Aggs_2_Layer_to_Matrix_and_indice(rs.aggs, "user_id", "name")
 
print result['rowIndexList']
print result['colIndexList']
print result['matrix']
 
fileTools = FileTools.FileTools()
fileTools.List_to_CSV(result['colIndexList'], "col_index.csv")
fileTools.Matrix_to_CSV(result['matrix'], "matrix.csv")



'''------------------------------------------- Agg to csv -------------------------------------------'''

conn=pyes.es.ES('localhost:9200')
q = pyes.MatchAllQuery()
tagg = pyes.aggs.TermsAgg('name', field= 'name', sub_aggs=[]) 
qsearch = pyes.query.Search(q) 
qsearch.agg.add(tagg)

rs = conn.search(query=qsearch , indices='example_index' ,type="example_type" )
print json.dumps(rs.aggs,indent=2)

fileTools = FileTools.FileTools()
fileTools.ES_Aggs_1_Layer_to_CSV(rs.aggs, "agg.csv", agg_name="name")