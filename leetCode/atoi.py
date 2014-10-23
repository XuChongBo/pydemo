class Solution:
    # @return an integer
    def atoi(self, str):
        x=0
        sign=1
        INT_MAX = 2147483647
        INT_MIN = -2147483648
        str = str.lstrip()
        for i in range(len(str)):
            ch=str[i]
            if i==0 and ch=='-':
                sign=-1
                continue
            if i==0 and ch=='+':
                continue

            if ch<'0' or ch>'9':
                break
            x=x*10+int(ch)

            if sign==-1 and x>=INT_MAX+1:
                return INT_MIN 
            if sign==1 and x>=INT_MAX:
                return INT_MAX 
                
        return sign*x

if __name__=="__main__":
    a = Solution()
    print a.atoi("aa")
    print a.atoi("-aa")
    print a.atoi("-3a")
    print a.atoi("+3a")
    print a.atoi(" -3a55")
    print a.atoi(" 10")
    print a.atoi(" +10")
    print a.atoi(" +1+0")
    print a.atoi("  -102")
    print a.atoi(" 30 204")
    print a.atoi("02b4")
    print a.atoi("2147483647")
    print a.atoi("2147483648")
    print a.atoi("-2147483647")
    print a.atoi("-2147483648")
    print a.atoi("-2147483649")
