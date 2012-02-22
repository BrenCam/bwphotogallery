# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# Define GAE datamodels for simple test
# Classes to link images to tags
# Classes for the collections

#    )
# Table definitions for GAE - multiple tags per image
#

user_id = 'test'

""" Tag can apply to many images """
db.define_table(
    'tag',
    Field('name'),
    Field('description', 'text')
    )

""" Image has many tags """
db.define_table(
    'image',
    Field('title'),
    Field('tag','list:reference tags'),
    #Field('created_by', db.auth_user, default=user_id, writable=False, readable=False),
    Field('created_on','datetime', default=request.now, writable=False, readable=False),
    Field('modified_on','datetime',default=request.now,writable=False,readable=False)
    )

db.image.tag.requires=IS_IN_DB(db(db.tag.id>0),'tag.id','%(name)s', multiple=True)
#db.image.tag.requires=IS_IN_DB(db(db.tag.created_by==auth.user_id),'tag.id','%(title)s', multiple=True)

# Join Table/Xref table - how to populate this ?
db.define_table(
    'imagetag',
    Field('image_id'),
    Field('tag_id')
    )

""" See py slice example  -   http://www.web2pyslices.com/slices/take_slice/16 """
db.define_table(
    'xtg',
    Field('name')
    )

db.define_table(
    'xim',
    Field('title')
    )

db.define_table(
    'xref',
    Field('xtg', db.xtg),
    Field('xim', db.xim)
    )
