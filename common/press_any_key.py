import time
import traceback



for i in range(8000):
    print i
    try:
        #shutil.copy(filepath, savefilepath); 
        1/0
        #Image.open(filepath).save(savefilepath , "PNG")
    except :
        print traceback.format_exc()
        raw_input('press any key to continue.')
    if i % 100 == 0:
         time.sleep(1)
