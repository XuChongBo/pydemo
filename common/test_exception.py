import time
import traceback

def zz():
    try:
        1/0
        #Image.open(filepath).save(savefilepath , "PNG")
    except :
        print traceback.format_exc()
        raw_input('press any key to continue.')
    if i % 100 == 0:
         time.sleep(1)

def aa():
    try:
        a = b
        #import xx
    except Exception,e:
        print e
        print traceback.format_exc()
    finally:
        print "something finally "



def tt():
    try:
        a = b
        #import xx
    except NameError, e:
        print e
    except :
        print traceback.format_exc()
    finally:
        print "something finally "
def ff():
    try:
       1/0
    except Exception,e:
       print traceback.format_exc()
       raise e
if __name__ == "__main__":
    #zz()
    #tt()
    #aa()
    ff()
