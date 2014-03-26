## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

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

#db.define_table=('images',  
#       Field('picture', 'upload', uploadfield='picture_file'),
#        Field('picture_file', 'blob')) 

db.define_table('image',
        Field('title', unique=True),
        Field('file', 'upload'),
        format = '%(title)s')

db.define_table('post',
        Field('image_id', 'reference image'),
        Field('author'),
        Field('email'),
        Field('body', 'text'))

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.post.author.requires = IS_NOT_EMPTY()
db.post.email.requires = IS_EMAIL()
db.post.body.requires = IS_NOT_EMPTY()

db.post.image_id.writable = db.post.image_id.readable = False
