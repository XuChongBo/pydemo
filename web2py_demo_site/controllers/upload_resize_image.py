#def test_images():
#    return HTML(BODY(
#        IMG(_src=URL('a_histogram'))))

from myplots import myplot
from myimagelib import resize_image

def do_resize():
    image_id = request.args[0]
    response.headers['Content-Type']='image/png'
    return resize_image()


def upload_resize():
    form = SQLFORM(db.image)
    img = None
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        #uploaded_image_record = db(db.image.id==form.vars.id).select()
        img = IMG(_src=URL('do_resize',args=form.vars.id))
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    #records = db().select(db.image.ALL)
    return dict(form=form, img=img)

def upload_show():
    form = SQLFORM(db.image)
    uploaded_image_record=[]
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        uploaded_image_record = db(db.image.id==form.vars.id).select()
        print uploaded_image_record
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    #records = db().select(db.image.ALL)
    return dict(form=form, records=uploaded_image_record)
