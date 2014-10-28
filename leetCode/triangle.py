class Solution_1:   #Time Limit Exceeded
    # @param triangle, a list of lists of integers
    # @return an integer
    def minimumTotal(self, triangle):
        s = self.getMinPath(triangle,0)
        return  s
    def getMinPath(self,triangle,rootPos):
        r = triangle[0][rootPos]
        child = triangle[1:]
        if not child: 
            return r
        left = self.getMinPath(child,rootPos)    
        right = self.getMinPath(child,rootPos+1)    
        if left>right:
            return right+r
        else:    
            return left+r

class Solution_2:
    def __init__(self):
        self.globalMin=100000

    # @param triangle, a list of lists of integers
    # @return an integer
    def minimumTotal(self, triangle):
        self.getMinPath(triangle,0,0)
        return  self.globalMin
    def getMinPath(self,triangle,rootPos,accu):
        r = triangle[0][rootPos]
        accu+=r
        print 'triangle:', triangle,"root:", rootPos,"globalMin:",self.globalMin,"accu:",accu
        if accu>=self.globalMin:
            return
        child = triangle[1:]
        print child
        if not child: 
            self.globalMin=accu
            return
        self.getMinPath(child,rootPos,accu)    
        self.getMinPath(child,rootPos+1,accu)    

class Solution:   #Time Limit Exceeded

    # @param triangle, a list of lists of integers
    # @return an integer
    def minimumTotal(self, triangle):
        self.cache_data={}
        s = self.getMinPath(triangle,0,0)
        return  s
    def getMinPath(self,triangle,deepLevel,rootPos):
        k="%s_%s" % (deepLevel,rootPos)
        if self.cache_data.has_key(k):
            return self.cache_data[k]
        r = triangle[0][rootPos]
        child = triangle[1:]
        if not child: 
            self.cache_data[k] = r
        else:
            left = self.getMinPath(child,deepLevel+1,rootPos)    
            right = self.getMinPath(child,deepLevel+1,rootPos+1)    
            if left>right:
                self.cache_data[k] =right+r
            else:    
                self.cache_data[k] =left+r

        return self.cache_data[k] 


#v,cur = min([(v,rootPos+i)for i,v in enumerate(layer[cur:cur+2])])
        
if __name__=="__main__":
    a = Solution()
    tree = [ [2],[3,4],[6,5,7],[4,1,8,3] ]
    print a.minimumTotal(tree)
    tree = [[-1],[2,3],[1,-1,-3]]
    print a.minimumTotal(tree)

