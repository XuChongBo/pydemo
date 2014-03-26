import os

def d():
    filename=request.args[0]
    path=os.path.join(request.folder,'uploads',filename)
    response.headers['ContentType'] ="application/octet-stream";
    response.headers['Content-Disposition']="attachment; filename="+filename
    return response.stream(open(path),chunk_size=4096)
    #return response.stream(open(filename),chunk_size=4096)
