
def index():
    link_list=[]
    base_url='http://'+request.env.http_host+'/'+request.application+'/'
    links = ["hello/action2","hello/action1"]
    links += ["form2/display_your_form"]
    links += ["form1/first","form1/second"]
    links += ["show_env/request","show_env/all"]
    links += ["form_crud/all_records","form_crud/update_your_form"]
    links += ["form_validation/display_your_form"]
    links += ["show_file/show"]
    for i in links:
        link_list.append((i, base_url+i))
    return dict(link_list=link_list)


def simple():
    return dict()

