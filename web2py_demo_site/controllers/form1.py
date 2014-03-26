
def first():
    form = SQLFORM.factory(Field('visitor_name',
                label='what is your name?',
                requires=IS_NOT_EMPTY()))
    if form.process().accepted:
        session.visitor_name = form.vars.visitor_name
        redirect(URL('second'))
    return dict(form=form)

def second():
    name = request.vars.visitor_name #or redirect(URL('first'))
    return dict(name=name)
