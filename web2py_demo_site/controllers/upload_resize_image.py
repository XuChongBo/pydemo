def upload_show():
    form = SQLFORM(db.image)
    uploaded_iamge_record=[]
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        uploaded_iamge_record = db(db.image.id==form.vars.id).select()
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    #records = db().select(db.image.ALL)
    return dict(form=form, records=uploaded_iamge_record)

def upload_resize():
    form = SQLFORM(db.image)
    uploaded_iamge_record=[]
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        uploaded_iamge_record = db(db.image.id==form.vars.id).select()
        print uploaded_image_record
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    #records = db().select(db.image.ALL)
    return dict(form=form, records=uploaded_iamge_record)
