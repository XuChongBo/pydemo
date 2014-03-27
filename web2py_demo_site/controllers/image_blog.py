def index():
    images = db().select(db.image.ALL, orderby=db.image.title)
    return dict(images=images)

def show():
    image = db.image(request.args(0,cast=int)) or redirect(URL('index'))
    db.post.image_id.default = image.id
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db(db.post.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

def download():
    return response.download(request, db)

def upload_and_show_all():
    form = SQLFORM(db.image)
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    records = db().select(db.image.ALL)
    return dict(form=form, records=records)


def upload_imagex():
    form = SQLFORM(db.image)
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
        #accepted values
        form.vars
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    records = db().select(db.image.ALL)
    return dict(form=form, records=records)
