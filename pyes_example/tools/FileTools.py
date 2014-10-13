import numpy

class FileTools(object):

    def ES_Aggs_1_Layer_to_CSV(self,esDict,filePath,agg_name = 'agg1', delimiter=','):
        
        f = file(filePath,"w")
            
        for item1 in esDict[agg_name].buckets:
            f.write(str(item1.key)+","+str(item1.doc_count)+"\n")
        
        f.close()
    
        
    def Matrix_to_CSV(self,matrix,filePath,delimiter=','):
        
        numpy.savetxt(filePath, matrix, delimiter=delimiter)
        
    def List_to_CSV(self,list,filePath):
        
        f = file(filePath,"w")
            
        for item in list:
            f.write(str(item)+'\n')
        
        f.close()