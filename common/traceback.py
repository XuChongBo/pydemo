import time
import traceback



for i in range(8000):
    print i
    try:
        #shutil.copy(filepath, savefilepath); 
        1/0
        #Image.open(filepath).save(savefilepath , "PNG")
    except Exception, e:
        print e
        print traceback.format_exc() # also you can call  logger.exception("some describe") 
        raw_input('press any key to continue.')
    if i % 100 == 0:
         time.sleep(1)
