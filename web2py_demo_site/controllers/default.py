
def index():
    link_list=[]
    base_url='http://'+request.env.http_host+'/'+request.application+'/'
    links = ["hello/action2","hello/action1"]
    links += ["form2/display_your_form"]
    links += ["form1/first","form1/second"]
    links += ["show_env/request","show_env/all"]
    links += ["form_crud/all_records","form_crud/update_your_form"]
    links += ["form_validation/display_your_form"]
    links += ["show_file/show_txt_file/test.txt"]
    links += ["show_file/show_image_file/test.png"]
    links += ["image_blog/index"]
    links += ["image_blog/upload_and_show_all"]
    links += ["upload_resize_image/upload_show"]
    links += ["upload_resize_image/upload_resize"]
    links += ["do_matplot"]
    for i in links:
        link_list.append((i, base_url+i))
    return dict(link_list=link_list)


def simple():
    return dict()

def download():  
    return response.download(request, db) 
