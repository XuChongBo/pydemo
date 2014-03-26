#db = DAL('sqlite://webform.sqlite')
#db.define_table('register',
#        Field('first_name', requires=IS_NOT_EMPTY()),
#        Field('last_name', requires=IS_NOT_EMPTY()),
#        Field('email', requires=IS_NOT_EMPTY()))
#

#db = DAL('sqlite://webform.sqlite')
#db.define_table('register',
#        Field('first_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
#        Field('last_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
#        Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()]))
#        db = DAL('sqlite://webform.sqlite')

db = DAL('sqlite://webform.sqlite')
db.define_table('register',
        Field('first_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
        Field('last_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
        Field('email', unique=True, requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
        Field('email_validate',requires=IS_EQUAL_TO(request.vars.email)))
db.register.email.requires=IS_NOT_IN_DB(db,'register.email')
