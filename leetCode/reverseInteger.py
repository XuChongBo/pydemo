class Solution:
    # @return an integer
    def reverse(self, x):
        sign=1
        y=0
        base=1
        if x<0:
            sign=-1
            x*=-1
        while(x>0):
            y=y*10+(x%10)
            x/=10
            
        #TODO: the reversed integer might overflow. raise an exception?
        return sign*y

if __name__=="__main__":
    a = Solution()
    print a.reverse(123)
    print a.reverse(-123)
    print a.reverse(123)
    print a.reverse(0)
    print a.reverse(-10)
    print a.reverse(-1023)
    print a.reverse(100)
