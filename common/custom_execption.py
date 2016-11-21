
import traceback
class ReadNullError(Exception):
    pass


try:
    if xxx
        raise ReadNullError("read null string")
        #或者直接用
        raise RuntimeError("socket connection broken")
except ReadNullError as e:
    print e
    print traceback.format_exc()
