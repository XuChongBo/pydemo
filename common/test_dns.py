#!/usr/bin/python  
#__*__ coding:utf-8 __*__  
#Filename:dns1.py  
  
  
import dns.resolver  
  
  
def main():  
    #domain = raw_input('Enter an domain:')  
    domain = 'tiku-online.zuoyetong.com.cn'
    #domain = 'tiku-online-test.zuoyetong.com.cn'
    A = dns.resolver.query(domain,'A') #指定查询类型为A记录  
    for i in A.response.answer:  #通过response.answer方法获取查询回应信息  
        for j in i.items:  
            print j  
  
      
if __name__=='__main__':  
    main()  
