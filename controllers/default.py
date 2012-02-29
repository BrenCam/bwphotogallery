# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py on GAE!"
    return dict(message=T('Hello From Google App Engine'))
    #response.write ('Hello From Google App Engine')

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
    
def list_images():
    #~ tags=db(db.tag.created_by==auth.user_id).select(orderby=db.tag.title)
    #images=db(db.image.id>0).select(orderby=db.image.title)
    images=db(db.xim.id>0).select(orderby=db.xim.title)
    return dict(images=images)
    
def edit_image():
    id=request.args(0)
    return dict(form=crud.update(db.image,id))

# Modify this to allow user to add/remove tags from an image
# need to handle mgmt of imgtag recs in parallel
# How/Where to define the form layout for this
#----------------------------------------------------------------------
def edit_image_tags():
    """
    ?? Need to create unbound form ??
    since I want to add/intercept save process
    
    """
    form = SQLFORM(db.image)
    #if form.validate():
        #if form.deleted:
            #db(db.image.id==record.id).delete()
        #else:
            #db(db.image.update_or_insertrecord(**dict(form.vars)
    
    


        
def add_image():

    form = SQLFORM(db.image)

    if form.accepts(request.vars, session): 
        response.flash='record inserted'

        image_id = dict(form.vars)['id']
        image = db(db.image.id==image_id).select()

        redirect(URL(r=request, f='list_images'))

    elif form.errors: response.flash='form errors'
    return dict(form=form)    
    
#~ @auth.requires_login()
def list_tags():
    #~ tags=db(db.tag.created_by==auth.user_id).select(orderby=db.tag.title)
    tags=db(db.tag.id>0).select(orderby=db.tag.name)
    return dict(tags=tags)
    
def list_by_image_imagetag():
    """ Use map table to list image tags """
    imgtags=db(db.imagetag.id>0).select(orderby=db.imagetag.image_id)
    rdict = {}
    taglist =[]
    for imgtag in imgtags:
        # get image rec + ##returns a list of recs for each image
        image =  db(db.image.id==imgtag.image_id).select().first()
        title = image.title
        #taglist = []            
        # build list of tag names
        #~ tagrecs = db(db.tag.id==imgtag.tag_id).select()
        tagrecs = db(db.imagetag.image_id==imgtag.image_id).select()
        for row in tagrecs:
            tag =  db(db.tag.id==row.tag_id).select().first()
            taglist.append(tag.name)
            #taglist.append('test')
        rdict[title] = taglist
        taglist =[]
    return dict(imgdict=rdict) 

    
def list_by_image():
    """ Display list of images ordered by tags """
    imgdict = {}
    # for each tag, find all images
    images=db(db.image.id>0).select(orderby=db.image.title)
    imglist = []
    for img in images:
        # possible bug here - getting 1 3 instead of 31 from result
        # s/b a ', sep list
        tl = db.image.tag.represent(img.tag)
        # split the result 
        tlist = tl.split(',')
        #response.write ('>>>>>>>  tlist: %s' %type(tl))
        #separate list
        for t in tlist:
            # ignore non numeric values
            try:
                x = int(t)
                if t in imgdict.keys():
                    imgdict[t].append(img.title)
                else:
                    imgdict[t] = [img.title]
            except:
                pass
    # dict of tag id's and list of associated images
    #replace dict with new version with tag names as the key
    dd2 = {}
    for k,v in imgdict.iteritems():
        #find tag name for tag id
        t=  db(db.tag.id==k).select().first()
        try:
            dd2[t.name] = v
        except:
            pass
    #return dict(imgdict=imgdict) 
    return dict(imgdict=dd2) 

def list_by_tag():
    # find images ordered by tag, display img + tag name
    # gae query requires a join here - ??how??
    images=db(db.image.id>0).select(orderby=db.image.title)
    imgdict = {}
    for img in images:
        tnames = []
        taglist = img.tag
        # need to get corresponding tag names (use map/lambda here?)
        for item in taglist:
            # Note: first is require here - else error
            t = db(db.tag.id==item).select().first()
            #tnames.append('zz')
            try:
                if t.id != 0:
                    tnames.append(t.name)            
            except:
                pass
                #~ tnames.append('')
            #tnames.append(t[0])
            #~ tnames.append(tag.name)
            #~ tnames.append(item)
        imgdict[img.title] = tnames
    return dict(imgdict=imgdict) 

#~ @auth.requires_login()
def edit_tag():
    id=request.args(0)
    return dict(form=crud.update(db.tag,id))

#~ @auth.requires_login()
def add_tag():

    form = SQLFORM(db.tag)

    if form.accepts(request.vars, session): 
        response.flash='record inserted'

        tag_id = dict(form.vars)['id']
        tag = db(db.tag.id==tag_id).select()

        redirect(URL(r=request, f='list_tags'))

    elif form.errors: response.flash='form errors'
    return dict(form=form)
    
def build_image_tag():
    # insert recs into map table
    images=db(db.image.id>0).select(orderby=db.image.title)
    itkeys=[]
    for img in images:
        tnames = []
        #taglist = img.tag
        tl = db.image.tag.represent(img.tag)
        # split the result 
        tlist = tl.split(',')
        for t in tlist:        
            # Note: first is require here - else error
            t = db(db.tag.id==t).select().first()
            tname = t.name
            itkey = db.imagetag.insert(image_id=img.id, tag_id=t.id)
            itkeys.append(itkey)
    response.write ('>>>>>>>  keys: %s' %itkeys)
  
  
#----------------------------------------------------------------------
def assign_newtag():
    """
    Create a new tag and assign to a image
    Create related imgtag entry
    """
    tag_id = db.tag.insert(name='newtag2', description='new tag test2 ')
    img_id = 12
    # ?? check data type check ??
    imgtag = db.imagetag.insert(image_id=img_id, tag_id=tag_id)
    return
        
#----------------------------------------------------------------------
def test_insert():
    """"""
    imglist = []
    img = db.imagetag.insert(image_id=99, tag_id=999)
    imglist.append(img)
    
    
#----------------------------------------------------------------------
def test_bulk_insert():
    
    # insert from a list of dicts
    ddlist = []
    d1 = {'image_id':10, 'tag_id':101 }
    d2 = {'image_id':10, 'tag_id':102 }
    d3 = {'image_id':11, 'tag_id':333 }
    ddlist.append(d1)
    ddlist.append(d2)
    ddlist.append(d3)
    
    imgids = db.imagetag.bulk_insert([d1],[d2],[d3])
    #imgids = db.imagetag.bulk_insert(**ddlist)
    
    #imgids = db.imagetag.bulk_insert(**ddlist)
    #imgids = db.imagetag.bulk_insert(*ddlist)
    
    #res = db.imagetag.bulk_insert(
        #*[{
        #'image_id': 111,
        #'tag_id': 1111
        #}]
    #)
    
    return
    
