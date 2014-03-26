def display_your_form():
    form = SQLFORM(db.register)
    return dict(form=form)
