
def print_gb(v):
    tmps = [(1024*1024*1024*1024, 'TB'), (1024*1024*1024, 'GB'), (1024*1024, 'MB'),  (1024, 'KB'), (1, 'B')]
    for base, s in tmps:
        if v >= base:
            print v*1.0/base, s
            return



gid_uid_num = 2*(10**7)

periods = 1 #+ 12 + 12*4 # 356  

featrue_n = 100 + (100 * 2  + 100 ) * periods  

print featrue_n 

cols_bytes = 4 + 4 + 32 + 4   # uid, gid, timestamp, key, value, version

print  'cols_bytes',
print_gb(cols_bytes)

persion_bytes = featrue_n * cols_bytes

print 'persion_bytes',
print_gb(persion_bytes)

total_bytes = persion_bytes * gid_uid_num

print 'total_bytes',
print_gb(total_bytes)
