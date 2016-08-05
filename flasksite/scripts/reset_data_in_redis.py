import traceback
import os
import sys
import time
import shutil
import redis
sys.path.append('../')
import config

data_dir = config.LABELED_DATASET_PATH
dict_filepath = "./handwriting.txt"

r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
r.flushdb()

# n = r.get("xxx")
# if n is None:
#     n = 0
# print n
# r.incr("xxx")
# sys.exit()
#############################  write hanzi list  #######################

def read_handwriting(filepath):
    import codecs
    with codecs.open(filepath, "r", 'utf-8') as myfile:
        line =  myfile.readline()
    print "read from ",filepath, "total:",len(line)
    return line



def write_hanzi_list():
    hanzi_list = read_handwriting(dict_filepath)
    #print hanzi_list
    for idx,tag in enumerate(hanzi_list):
        print idx, tag.encode('utf-8')
        r.rpush('hanzi_list',tag.encode('utf-8'))

write_hanzi_list()



#############################  write hanzi list  #######################
def write_stat_count_to_redis(category, num):
    k  = category+"_count"
    r.set(k, num)




data_dir = data_dir.rstrip("/")
total = 0
stat_by_hanzi = {}
paths_by_hanzi = {}
stat_by_imei = {}
for root, dirs, files in os.walk(data_dir):
    for filename in files:
        if filename.endswith('.png'):
            total += 1
            imei =  filename.split("_")[2]
            filepath = os.path.join(root, filename)
            hanzi =  filepath.split("/")[-2]
            print hanzi
            print filepath

            paths_by_hanzi.setdefault(hanzi, [])
            paths_by_hanzi[hanzi].append(filepath)

            stat_by_hanzi.setdefault(hanzi, 0)
            stat_by_hanzi[hanzi] +=1
            
            stat_by_imei.setdefault(imei, 0)
            stat_by_imei[imei] +=1

print stat_by_hanzi
print 'total:',total

r.set("total_count", total)

num1 = 0
for k in stat_by_hanzi:
    print k, stat_by_hanzi[k],
    num1 += stat_by_hanzi[k]
    write_stat_count_to_redis(k, stat_by_hanzi[k])

print 

num2 = 0
for k in stat_by_imei:
    print k, stat_by_imei[k],
    num2 += stat_by_imei[k]
    write_stat_count_to_redis(k, stat_by_imei[k])
print 

num3 = 0
for k in paths_by_hanzi:
    for path in paths_by_hanzi[k]:
        num3 += 1
        r.rpush(k+"_pathlist",path)
print 



print total, num1, num2, num3


