def display_your_form():
    form = SQLFORM(db.register)
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    else:
        response.flash = 'Try again - no fields can be empty.'
    return dict(form=form)
