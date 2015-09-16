import lmdb
import numpy as np
import numpy as np
from pprint import pprint

db = lmdb.open('lmdb_file')

pprint(db.stat())

with db.begin(write=True, buffers=True) as txn:
    txn.put('foo', 'bar') 
    buf = txn.get('foo')           # only valid until the next write.
    buf_copy = bytes(buf)          # valid forever
    txn.put('foo2', 'bar2')        # this is also a write!
    txn.delete('foo')              # this is a write!

    txn.put('foo3', 'bar3')        # this is also a write!

    print('foo: %r' % (buf,))      # ERROR! invalidated by write
    print('foo: %r' % (buf_copy,)) # OK

    lmdb_cursor = txn.cursor()

    for key, value in lmdb_cursor:
        print key,value
    pprint(db.stat())

print('foo: %r' % (buf,))          # ERROR! also invalidated by txn end
print('foo: %r' % (buf_copy,))     # still OK
pprint(db.stat())

db.close()

