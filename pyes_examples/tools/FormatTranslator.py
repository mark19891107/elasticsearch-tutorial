

class FormatTranslator(object):

    def ES_Aggs_2_Layer_to_Matrix_and_indice(self,esDict,agg1_name="agg1",agg2_name="agg2"):
        
        rowIndexList =[]
        colIndexList = []
        matrix = []
        result = {}
    
        for item1 in esDict[agg1_name].buckets:
            rowIndexList.append(item1.key)
            for item2 in item1[agg2_name].buckets:
                if item2.key not in colIndexList:
                    colIndexList.append(item2.key)
                    
                
        for i in range(0,len(rowIndexList)):
            matrix.append(([0.0]*len(colIndexList)))
            
        for item1 in esDict[agg1_name].buckets:
            for item2 in item1[agg2_name].buckets:
                matrix[rowIndexList.index(item1.key)][colIndexList.index(item2.key)] = float(item2.doc_count)
        
        result['rowIndexList'] = rowIndexList
        result['colIndexList'] = colIndexList
        result['matrix'] = matrix
        
        return result
    
    def ES_Aggs_2_Layer_to_Numpy_Matrix(self,esDict,agg1_name="agg1",agg2_name="agg2"):
        
        return self.ES_Aggs_2_Layer_to_Matrix_and_indice(esDict,agg1_name,agg2_name)['matrix']