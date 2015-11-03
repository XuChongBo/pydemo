from fabric.api import run,execute
import time

def get_result(lines, process_id):
    #get result         
    for line in lines:
        items = line.split()
        #print items
        #items.append(" ")
        if len(items)>=14 and items[12]=="result:":
            id = items[10][:-1]
            if len(items)>=15:
                ocr_result = " ".join(items[14:-1])
            else:
                ocr_result = "NULL"
            if id==process_id:
                #print "got: ", id, ocr_result
                return ocr_result
    return None

last_id = 0
def get_task(lines):
    global last_id
    for line in lines:
        items = line.split()
        #print items        
        if len(items)>=13 and items[11]=="Downloading":
            id =  items[10]
            url = items[12]
            req_url = get_request_url(lines, id)            
    #print id, url
    if last_id!=id and req_url:
        last_id = id
        return (id,url,req_url)  
    return (0,"","")


def get_request_url(lines, process_id):
    global last_id
    for line in lines:
        items = line.split()
        #print items        
        if len(items)>=12 and items[11][:8]=="url=http":
            id =  items[10][:-1]
            #print items[11]
            if id==process_id:
                url = items[11][7:]            
                return url
    return None

def check_remote_log(socketio):
    execute(__check_remote,socketio, hosts=["xucb@180.150.190.52:666"])
def __check_remote(socketio): 
    process_id = 0
    process_url = ""
    req_url = ""
    REMOTE_PATH = '/data/ocr/ocr_service/logs'
    patient = 0 
    count = 0
    while True:
        remote_filename = REMOTE_PATH+'/'+'ocr_20151102.log' 
        #local_filename  = LOCAL_PATH +'_logs/'+'audit_logSessionServer.txt' + '.'+env.host

        remote_ret = run(""" tail  -n100 %s | grep -E 'Downloading http|Return result|url=http' """ % remote_filename)
        lines =  remote_ret.split('\n');
        if process_id==0:
            process_id,process_url,req_url = get_task(lines)
        ocr_result = get_result(lines, process_id)
        if ocr_result is not None:
            print "got: ", patient, process_id, process_url,  ocr_result,req_url
            out_str = process_id +"</br>"+req_url+"</br>"+ process_url+"</br>" + ocr_result
            count += 1 
            socketio.emit('my response',
                      {'data': out_str, 'count': count, 'image_url':process_url},
                      namespace='/test') 
            process_id, process_url,req_url = get_task(lines)
            patient = 0
        print "processing:", process_id, patient, process_url
        patient+=1
        if patient>5:
            process_id=0        
        time.sleep(2)

def test(): 
    process_id = 0
    process_url = ""
    req_url = ""
    REMOTE_PATH = '/data/ocr/ocr_service/logs'
    patient = 0 
    while True:
        remote_filename = REMOTE_PATH+'/'+'ocr_20151102.log' 
        #local_filename  = LOCAL_PATH +'_logs/'+'audit_logSessionServer.txt' + '.'+env.host

        remote_ret = run(""" tail  -n100 %s | grep -E 'Downloading http|Return result|url=http' """ % remote_filename)
        lines =  remote_ret.split('\n');
        if process_id==0:
            process_id,process_url,req_url = get_task(lines)
        ocr_result = get_result(lines, process_id)
        if ocr_result is not None:
            print "got: ", patient, process_id, process_url,req_url,  ocr_result
            process_id, process_url,req_url = get_task(lines)
            patient = 0
        print "processing:", process_id, patient, process_url
        patient+=1
        if patient>5:
            process_id=0        
        time.sleep(2)

if __name__ == '__main__':
    execute(test, hosts=["user@host:port"])
