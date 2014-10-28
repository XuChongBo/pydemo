class Solution:
    # @param A, a list of integer
    # @return an integer
    def singleNumber(self, A):
        d={}
        for i in A:
            if d.has_key(i):
                d.pop(i)
            else:
                d[i]=True
        return d.keys()[0]            

if __name__=="__main__":
    a = Solution()
    print a.singleNumber([1, 4, 1])
    print a.singleNumber([1,1,1,1,4, 4, 1])
    print a.singleNumber([1,2,3,4,5,5,4,3,2,1,8])
