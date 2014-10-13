<html>

<xmp theme="united" style="display:none;">
# pyes API



- [Simple Example](#Simple_Example)
	- [Create Connection](#Creat_Connection)
	- [Index Data](#Index_Data)
		- [Sample Dataset](#Sample_Dataset)
	- [Create Simple Query](#Creat_Simple_Query)
	- [Create Simple Aggregation](#Creat_Simple_Aggregation)
	- [Get Results](#Get_Results)
	
- [Connection](#Connection)
	- [Simple Connection](#Simple_Connection)
	- [Connection With Basic Auth](#Connection_With_Basic_Auth)
	
- [Query](#Query)
	- [Match All Query](#Match_All_Query)
	- [Term Query](#Term_Query)
	- [Range Query](#Range_Query)
	- [Boolean Query](#Boolean_Query)
	
- [Filter](#Filter)
	- [Terms Filter](#Terms_Filter)
	- [Terms Filter with Terms Lookup](#Terms_Filter_with_Terms_Lookup)
	- [Boolean Filter](#Boolean_Filter)
	
- [Aggreation](#Aggreation)
	- [Term Aggregation](#Term_Aggregation)
	- [Date Histogram Aggregation](#Date_Histogram_Aggregation)
	- [Statistic Aggregation](#Statistic_Aggregation)
	
- [Format Translator](#Format_Translator)
	- [ES aggs 2 layers to Matrix](#ES_aggs_2_layers_to_double[][]_Matrix)
	
- [Files tools](#Files_tools)
	- [ES aggs 1 layer to CSV](#ES_aggs_1_layer_to_CSV)
	- [Matrix to CSV](#Double[][]_Matrix_to_CSV)




##<a id="Simple_Example"></a>Simple Example
以下內容是一個簡單的範例，看完以下內容後在針對每一個小塊，去看後面張傑更詳細的介紹或是變化．每一個區塊都可以獨立帶換掉，組成不同的效果．在執行下列程式碼之前，記得先 import 以下 libraries．
	
	import json
	from pyes import ES,MatchAllQuery
	from pyes.aggs import TermsAgg
	# 以下兩個 tool 是自己寫的 ＸＤ
	from tools.FileTools import FileTools
	from tools.FormatTranslator import FormatTranslator
	
###<a id="Creat_Connection"></a>Create Connection
connection 顧名思義是用來與 ES 建立連線．之後所有的 index ( 新增 ) 與 Query ( 查詢 ) 都會使用 connection 物件．
	# 最簡單的connection就是連接 localhost:9200 ，但是因為預設就是這些值，所以可以不用打
	conn = ES()
###<a id="Index_Data"></a>Index Data
以下是簡單的新增資料的做法，讀入資料為 JSON 格式．放入 index 指令中．第二欄位是要新增的 index 名稱，再來是 type 然後 id ．

	dataset_json = open("../dataset.json")
	dataset = json.load(dataset_json)['data']
	for data in dataset:
    	conn.index(data, "example_index", "example_type", "example_id_"+str(dataset.index(data)))

####<a id="Sample_Dataset"></a>Sample Dataset
以下是範例的 dataset ，另存成 dataset.json 給上面的 code 吃

    {
      "data": [
        {
          "date": "2014-09-13",
          "name": "Mary Jones",
          "tweet": "Elasticsearch means full text search has never been so easy",
          "user_id": 2
        },
        {
          "date": "2014-09-14",
          "name": "John Smith",
          "tweet": "@mary it is not just text, it does everything",
          "user_id": 1
        },
        {
          "date": "2014-09-15",
          "name": "Mary Jones",
          "tweet": "However did I manage before Elasticsearch?",
          "user_id": 2
        },
        {
          "date": "2014-09-16",
          "name": "John Smith",
          "tweet": "The Elasticsearch API is really easy to use",
          "user_id": 1
        },
        {
          "date": "2014-09-17",
          "name": "Mary Jones",
          "tweet": "The Query DSL is really powerful and flexible",
          "user_id": 2
        },
        {
          "date": "2014-09-18",
          "name": "John Smith",
          "user_id": 1
        },
        {
          "date": "2014-09-19",
          "name": "Mary Jones",
          "tweet": "Geo-location aggregations are really cool",
          "user_id": 2
        },
        {
          "date": "2014-09-20",
          "name": "John Smith",
          "tweet": "Elasticsearch surely is one of the hottest new NoSQL products",
          "user_id": 1
        },
        {
          "date": "2014-09-21",
          "name": "Mary Jones",
          "tweet": "Elasticsearch is built for the cloud, easy to scale",
          "user_id": 2
        },
        {
          "date": "2014-09-22",
          "name": "John Smith",
          "tweet": "Elasticsearch and I have left the honeymoon stage, and I still love her.",
          "user_id": 1
        },
        {
          "date": "2014-09-23",
          "name": "Mary Jones",
          "tweet": "So yes, I am an Elasticsearch fanboy",
          "user_id": 2
        },
        {
          "date": "2014-09-24",
          "name": "John Smith",
          "tweet": "How many more cheesy tweets do I have to write?",
          "user_id": 1
        }
      ]
    }

###<a id="Creat_Simple_Query"></a>Create Simple Query
Query 是一次查詢中必要的角色，在這邊使用 Match All 就是全拿

	query = MatchAllQuery()
###<a id="Creat_Simple_Aggregation"></a>Create Simple Aggregation
Aggregation 是用來 summarize 資訊的方法，在這邊使用的是相同 term 的個數統計． sub_aggs是留給如果要在進一步作第二層 aggregation 時使用的， size 則是要顯示 aggregation 後的前幾名 ( 100 就是前 100 名 )

	agg = TermsAgg('agg1', field="name",sub_aggs=[],size=100)

###<a id="Get_Results"></a>Get Results
在pyes中取得搜尋內容的方式如下，要注意的是在預設的情況下 pyes 是不希望使用者一口氣拉回所有資料，所以要採用一筆一筆的方式拿出來．使用 Search 物件將 query 以及 agg 兩個部分包在一起．Search 物件所定義的 size 是表示Query 出來筆數限制．
	
	# 加入 query 以及 aggs 資訊進入 Search 中，並且可以用 .serialize() 印出現階段語法，檢視當前的語法是否正確
	search = Search(query,size=5)
	search.agg.add(agg)
	print search.serialize()
	
	# 創造出 ResultSet 物件
	# 注意！！！！在現階段並沒有真正去做進 ES 查詢的動作
	# 要在之後要讀取 result 的內容時才會真正去查詢
	result = conn.search(search, "example_index", "example_type" )
	
	# 依序印出每一筆查詢結果，以及印出 aggregation 的結果
	# 使用 json.dumps(XXXXXXX,indent=2) 只是為了好閱讀
	# 這邊使用 search.size 而不是使用 len(result) 是因為後者永遠是表示總共搜尋到幾篇文章
	# 前者是表示要顯示幾筆結果。當已經限制顯示數量時，就不能用 .next() 走到限制筆數之外！
	# 當然也可以直接用 for XXX in result: 的寫法確保不要走超過！
	# 這邊 aggregation 的結果會發現名字會被拆開，是因為我們是對 term 做，而 ES 本身會做段詞，所以名字都會被拆成個別的 terms
	for i in range(0,search.size):
    	print json.dumps(result.next(),indent=2)
	print json.dumps(result.aggs,indent=2)

	# 若是硬要一口氣取得所有結果自己做 parse 可偷偷呼叫下列隱藏 function 以及隱藏屬性
	result._do_search()
	print json.dumps(result._results,indent=2)
	
	

##<a id="Connection"></a>Connection

###<a id="Simple_Connection"></a>Simple Connection

	#一開始要先
	import pyes
	#以下會列出所有的路徑，所以這份文件看不到 "from pyes import *"
	conn=pyes.es.ES('localhost:9200') #domain:port

###<a id="Connection_With_Basic_Auth"></a>Connection With Basic Auth
	
	conn=pyes.es.ES('http://localhost:9200' ,basic_auth={'username':'username','password':'password'},timeout=100, max_retries=30, bulk_size=2,default_indices='facebook',default_types='opinion' )

##<a id="Query"></a>Query

###<a id="Match_All_Query"></a>Match All Query
	import pyes
	
	conn = pyes.es.ES('localhost:9200')
	q = pyes.query.MatchAllQuery()
	
	result = conn.search(query=q , indices='example_index' , doc_types='example_type') 
	# indice與doc_types可以使用多重選擇，但記得要用[]包起來。
	
	for i in result:
		print i
	# 用迴圈可以把結果印出來。

###<a id="Term_Query"></a>Term Query
	import pyes
	
	conn = pyes.es.ES('localhost:9200')
	
	# 在這邊要特別注意， dataset 中的人物叫 "J"ohn 但是查詢的時候要打 "j"hon
	# ES 不分大小寫，但是查詢只能用小寫！！
	tq = pyes.query.TermQuery(field="name", value="john")
	
	result = conn.search(query=tq, indices='example_index' , doc_types='example_type')
	for i in result:
		print i

###<a id="Range_Query"></a>Range Query
	import pyes
	
	conn = pyes.es.ES('localhost:9200')
	ESR = pyes.ESRange(field="date", from_value="2014-09-15", to_value="2014-09-18", include_lower=True ,include_upper=False)
	# 因為 include_upper 是 False 所以 upper bound 並不會被包含 ( 結果不會有 2014-09-18 )
    
    rq = pyes.query.RangeQuery(qrange=ESR)
    
    result = conn.search(query=rq, indices='example_index' , doc_types='example_type')
    for i in result:
		print i
    

###<a id="Boolean_Query"></a>Boolean Query
	import pyes
	
	conn = pyes.es.ES('localhost:9200')
	bq = pyes.query.BoolQuery() 
	# BoolQuery本身是一個Query的組合，可以使用add_must(), add_must_not(), add_should()來使用。
	
	bq.add_must(pyes.query.TermQuery("tweet","elasticsearch")) #(field, term)
	bq.add_must_not(pyes.query.TermQuery("name","john")) #(field, term)
	# tweet 包含 elasticsearch 但是作者不是 John ( 注意大小寫！！ )
	
	result = conn.search(query=bq, indices='example_index' , doc_types='example_type') 
	#使用Boolquery來當query的值。
	
	for i in result:
		print i

##<a id="Filter"></a>Filter

###<a id="Terms_Filter"></a>Terms Filter
	# 有兩種方式來query,分別為TermFilter與TermsFilter。兩者的差別為一個term與多個term的query。所以其實可以都用TermsFilter。
	import pyes
	 
	conn = pyes.es.ES('localhost:9200')
	tf  = pyes.filters.TermFilter(field="tweet", value="elasticsearch")
	tsf = pyes.filters.TermsFilter(field="tweet", values=["elasticsearch","easy"]) 
	# values後面等於的東西一定要加[]
	
	fq=pyes.query.FilteredQuery(pyes.query.MatchAllQuery(), tsf) 
	# 要把filter拿去做query必須要以FilteredQuery來query。
	
	result = conn.search(query= fq, indices="example_index" , doc_types="example_type")
	for i in result:
		print i
	
	# 由輸出結果可知 filter 多個值得時候，他們是採用 or 而不是 and 因此只要出現其中一個 term 就算有比對成功。
	
###<a id="#Terms_Filter_with_Terms_Lookup"></a>Terms Filter with Terms Lookup

	import pyes

	conn = pyes.es.ES('localhost:9200')
	conn.index({"list":["elasticsearch","easy"]}, "example_index", "example_type", "terms_list")

	# 使用 Terms Lookup 載入 List
	tl = pyes.TermsLookup(index="example_index", type="example_type", id="terms_list", path='list')
	tsf = pyes.filters.TermsFilter("tweet",tl)
	fq=pyes.query.FilteredQuery(pyes.query.MatchAllQuery(), tsf) 
	
	result = conn.search(query= fq, indices="example_index" , doc_types="example_type")
	for i in result:
	    print i
	
###<a id="Boolean_Filter"></a>Boolean Filter
	#BoolFilter本身是一個Query的組合，可以使用add_must(), add_must_not(), add_should()來使用。
	import pyes

	conn = pyes.es.ES('localhost:9200')
	bf = pyes.filters.BoolFilter()
	bf.add_must(pyes.filters.TermFilter("tweet","elasticsearch"))
	bf.add_must(pyes.filters.TermFilter("tweet","easy"))
	fq=pyes.query.FilteredQuery(pyes.query.MatchAllQuery(), bf)

	result = conn.search(query= fq, indices="example_index" , doc_types="example_type")
	for i in result:
    	print i


##<a id="Aggreation"></a>Aggreation

###<a id="Term_Aggregation"></a>Term Aggregation

	import pyes
	import json
	# 單層集合（做兩個不同aggregation）
	conn = pyes.es.ES('localhost:9200')
	q = pyes.query.MatchAllQuery()
	tagg = pyes.aggs.TermsAgg('name', field= 'name') 
	tagg1 = pyes.aggs.TermsAgg('user_id', field= 'user_id')
	# 需要給一個名字給出來集合。

	qsearch = pyes.query.Search(q) 
	# 要做aggregation需要使用Search,因為他裡面有一個.agg。
	# 不管是如何一定要有query的方式，此以MatchAllQuery()作為query方式。
	# This "Search" is under pyes.query, http://pydoc.net/Python/pyes/0.99.5/pyes.query

	qsearch.agg.add(tagg) 
	qsearch.agg.add(tagg1)
	# 將aggregation的方法加入到qsearch.agg裡面
	
	rs = conn.search(query=qsearch,index='example_index',type="example_type") 
	print json.dumps(rs.aggs,indent=2) 
	# 我們要的結果
	
	===========================================================================================
	
	# 雙層集合(階層集合)（注意sub_aggs，重點）
	conn=pyes.es.ES('localhost:9200')
	q = pyes.MatchAllQuery()
	tagg = pyes.aggs.TermsAgg('user_id', field= 'user_id', sub_aggs=[]) 
	tagg1 = pyes.aggs.TermsAgg('name', field= 'name')  
	tagg.sub_aggs.append(tagg1) 
	# 將tagg1加到tagg.sub_aggs裡面。
	qsearch = pyes.query.Search(q) 
	# This "Search" is under pyes.query, http://pydoc.net/Python/pyes/0.99.5/pyes.query
	qsearch.agg.add(tagg)

	rs = conn.search(query=qsearch , indices='example_index' ,type="example_type" )
	print json.dumps(rs.aggs,indent=2)

	
###<a id="Date_Histogram_Aggregation"></a>Date Histogram Aggregation
	import pyes
	import json
	conn=pyes.es.ES('localhost:9200')
	q = pyes.MatchAllQuery()
	DHAgg = pyes.aggs.DateHistogramAgg('3date' ,field='date', interval='3d') 
	# 給名字、field、與interval。field必須是時間格式的。
	qsearch = pyes.Search(q)  
	qsearch.agg.add(DHAgg)

	rs = conn.search(query=qsearch ,indices='example_index' ,type="example_type" )
	print json.dumps(rs.aggs,indent=2)

###<a id="Statistic_Aggregation"></a>Statistic Aggregation

以下統計的範例因為 dataset 中沒有形態是"數值"的欄位，所以使用 user_id 來練習。

	import pyes
	import json
	conn=pyes.es.ES('localhost:9200')
	q = pyes.MatchAllQuery()
	SumAgg = pyes.aggs.SumAgg('sum' ,field='user_id') 
	AvgAgg = pyes.aggs.AvgAgg('sum' ,field='user_id') 
	MaxAgg = pyes.aggs.MaxAgg('sum' ,field='user_id') 
	MinAgg = pyes.aggs.MinAgg('sum' ,field='user_id') 
	# 給名字、field、與interval。field必須是時間格式的。
	qsearch = pyes.Search(q)  
	qsearch.agg.add(SumAgg)

	rs = conn.search(query=qsearch ,indices='example_index' ,type="example_type" )
	print json.dumps(rs.aggs,indent=2)
	# 因為 user 1 跟 2 個發過 6 篇文章 所以加總會是 18

##<a id="Format_Translator"></a>Format Translator
以下的工具為自行開發的，不是 pyes 中的。如有需要請跟別人索取

###<a id="ES_aggs_2_layers_to_double[][]_Matrix"></a>ES aggs 2 layers to Matrix

	import pyes
	import json
	import FormatTranslator

	conn=pyes.es.ES('localhost:9200')
	q = pyes.MatchAllQuery()
	tagg = pyes.aggs.TermsAgg('user_id', field= 'user_id', sub_aggs=[]) 
	tagg1 = pyes.aggs.TermsAgg('name', field= 'name')  
	tagg.sub_aggs.append(tagg1) 
	qsearch = pyes.query.Search(q) 
	qsearch.agg.add(tagg)

	rs = conn.search(query=qsearch , indices='example_index' ,type="example_type" )
	print json.dumps(rs.aggs,indent=2)

	# 使用工具將兩層 aggs 的結果轉換成矩陣表示（ 包含 row index , col index , matrix 三個部分）
	# 在轉換時要告知 aggs 所使用的名稱 ( 不是 fields 是"名字" )
	formatTranslator = FormatTranslator.FormatTranslator()
	result = formatTranslator.ES_Aggs_2_Layer_to_Matrix_and_indice(rs.aggs, agg1_name="user_id", agg2_name="name")

	print result['rowIndexList']
	print result['colIndexList']
	print result['matrix']


##<a id="Files_tools"></a>Files tools

###<a id="ES_aggs_1_layer_to_CSV"></a>ES aggs 1 layer to CSV

	import pyes
	import json
	import FormatTranslator
	import FileTools
	
	conn=pyes.es.ES('localhost:9200')
	q = pyes.MatchAllQuery()
	tagg = pyes.aggs.TermsAgg('name', field= 'name', sub_aggs=[]) 
	qsearch = pyes.query.Search(q) 
	qsearch.agg.add(tagg)

	rs = conn.search(query=qsearch , indices='example_index' ,type="example_type" )
	print json.dumps(rs.aggs,indent=2)

	fileTools = FileTools.FileTools()
	fileTools.ES_Aggs_1_Layer_to_CSV(rs.aggs, "agg.csv", agg_name="name")
###<a id="Double[][]_Matrix_to_CSV"></a>Matrix to CSV

	import pyes
	import json
	import FormatTranslator
	import FileTools

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
	result = formatTranslator.ES_Aggs_2_Layer_to_Matrix_and_indice(rs.aggs, agg1_name="user_id", agg2_name="name")
	
	# 使用工具將結果儲存起來
	fileTools = FileTools.FileTools()
	fileTools.List_to_CSV(result['colIndexList'], "col_index.csv")
	fileTools.List_to_CSV(result['rowIndexList'], "row_index.csv")
	fileTools.Matrix_to_CSV(result['matrix'], "matrix.csv")
	
    
</xmp>
<script src="http://strapdownjs.com/v/0.2/strapdown.js"></script>
</html>