import os


# items of a checker
def a0(d):
    print 'check a0'

def a1(d):
    print 'check a1'

def b1(d):
    print 'check b1'

def a2(d):
    print 'check a2'

def b0(d):
    print 'check b0'

def c0(d):
    print 'check c0'

def docheck(checker,d,curKey='root'):
    """
    check the dict d using checker. 
    The d and check have the same keys in tree 
    """
    if not isinstance(d,dict):
        print 'error: value for key - %s needs to be a dict' % curKey
        return
    for k in checker.keys():
        #step1. check if the key exists
        v=d.get(k,None)  
        if v==None:
            print 'error:has no key -', k
            continue
        #step2. check if the func is dict
        func=checker[k]
        if isinstance(func,dict):
            docheck(func,v,k)
        else:
            func(v)
        #step3. do extra things  for special key
        #if k==''


#print getattr(__main__,'a0')
#print d.keys(), d.values()
check1={'a0':a0,'b0':b0,'c0':c0}
check2={'a1':a1,'b1':b1}

check3={'a0':a0,'b0':b0}
check3['c0']=check2

print '===check1 data1========'
data1={'a0':1, 'b0':{'a1':3,'b1':4,'c1':{'a2':12}},'c0':23,'d0':{'a1':3,'b1':4}}
docheck(check1,data1)

print '===check1 data2========'
data2={'x':2,'y':{'a0':33}}
docheck(check1,data2)

print '===check1 data3========'
data3={'a0':1, 'b0':{'a1':3,'c1':{'a2':12}},'c0':23,'d0':{'a1':3,'b1':4}}
docheck(check1,data3)

print '===check3 data3========'
docheck(check3,data3)

print '===check3 data4========'
data4={'a0':1, 'b0':{'a1':3,'c1':{'a2':12}},'xx':23,'c0':{'a1':3,'b1':4}}
docheck(check3,data4)

print '===check1 data5========'
data5=999
docheck(check1,data5)
