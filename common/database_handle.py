#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys  
sys.path.append('/Users/xcbfreedom/projects/web2py/web2py.app/Contents/Resources/')   

from gluon.dal import DAL,Field
from gluon.sqlhtml import SQLFORM
from gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_LENGTH
 

db = DAL("sqlite://data/mydb.sqlite")
db.define_table('t_contact', 
                         Field("name"),
                         Field("email"),
                         Field("phone"))
db.t_contact.name.requires = IS_NOT_EMPTY()
db.t_contact.email.requires = IS_EMAIL()
db.t_contact.phone.requires = IS_LENGTH(14)
     
#====insert 
print db.t_contact.insert(**dict(name="fx", email="x.comll", phone='123'))
print db.t_contact.insert(**dict(name="axbc", email="x.comll", phone='123'))
db.commit()
print 'insert ok'

#====select
print "select "
print db(db.t_contact.phone=='123').select()
print "select one"
print db.t_contact(**dict(phone='123'))

