def show_txt_file():
    import os
    filename=request.args[0]
    path=os.path.join(request.folder,'uploads',filename)
    f=open(path)
    lines=f.readlines()
    t="</br>".join(lines)
    #t.replace('\n',"""</br>""")
    return t


def show_image_file():
    import os
    filename=request.args[0]
    path=os.path.join(request.folder,'uploads',filename)
    return response.stream(open(path,'rb'))
