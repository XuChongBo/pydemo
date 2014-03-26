def all_records():
    #to show all the records
    grid = SQLFORM.grid(db.register,user_signature=False)
    return locals()

def update_your_form():
    #http://127.0.0.1:8000/demo/form_crud/update_your_form/3
    update = db.register(request.args)
    form = SQLFORM(db.register, update)
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    else:
        response.flash = 'Try again - no fields can be empty.'
 
