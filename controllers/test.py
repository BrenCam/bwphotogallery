# test controller for gae join
if 0:
    import db, request, response

#----------------------------------------------------------------------
def load():
    """"""
    
    # Delete any current recs
    db(db.xtg.id>0).delete()    
    db(db.xim.id>0).delete()
    db(db.xref.id>0).delete()
    
    # create some test data
    # Tags
    tg_uk = db.xtg.insert(name='UK')
    tg_us = db.xtg.insert(name='US')
    tg_eu = db.xtg.insert(name='EU')
    tg_ir = db.xtg.insert(name='IR')
    tg_fr = db.xtg.insert(name='FR')    
    
    # images
    ig_a = db.xim.insert(title='London')
    ig_b = db.xim.insert(title='Manchester')
    ig_c = db.xim.insert(title='New York')
    ig_d = db.xim.insert(title='Paris')
    ig_e = db.xim.insert(title='Dublin')
    ig_f = db.xim.insert(title='Dubai')
    ig_g = db.xim.insert(title='Delhi')
    ig_h = db.xim.insert(title='Lisbon')
    
    # xref
    db.xref.insert(xim=ig_a, xtg= tg_uk)
    db.xref.insert(xim=ig_a, xtg= tg_eu)
    
    db.xref.insert(xim=ig_b, xtg= tg_uk)
    db.xref.insert(xim=ig_b, xtg= tg_eu)
    
    db.xref.insert(xim=ig_c, xtg= tg_us)
    
    db.xref.insert(xim=ig_d, xtg= tg_fr)
    db.xref.insert(xim=ig_d, xtg= tg_eu)
    
    db.xref.insert(xim=ig_e, xtg= tg_ir)
    db.xref.insert(xim=ig_e, xtg= tg_eu)
    db.xref.insert(xim=ig_h, xtg= tg_eu)
    return
       
#----------------------------------------------------------------------
def query_by_tag():
    """
    get all images for a tag
    """
    
    #rows = (db(purchase.buyer==kenny).select()|db(purchase.buyer==cartman).select())
    
    # find matches by tag
    cnt = 0
    tg_eu = db(db.xtg.name=='EU').select().first()
    rows = (db(db.xref.xtg==tg_eu.id).select())
    #rows = (db(db.xref.xtg==tg_eu.id).select()).as_list()
    imglist = []
    for r in rows:
        cnt +=1
        imglist.append(r.xim.title)
        
    return

#----------------------------------------------------------------------
def query_by_img():
    """
    get all tags for an image
    """
    cnt = 0
    img = db(db.xim.title=='Paris').select().first()
    rows = (db(db.xref.xim==img.id).select())
    tlist = []
    for r in rows:
        cnt +=1
        tlist.append(r.xtg.name)
        
    return

def list_by_tag():
    """
    build a dict of tags and related images
    """
    tags = db(db.xtg.id>0).select()
    tagdict = {}    
    for tag in tags:
        rows = (db(db.xref.xtg==tag.id).select())
        tlist = []
        for r in rows:
            tlist.append(r.xim.title)
        # key is a tuple of tag name and tag count a
        # ?? key needs to include pk of the tag rec for future reference 
        # nested tuple value
        tpl = (tag.id,tag.name)      
        dk = (tpl,len(tlist))
        #dk = (tag.name,len(tlist))
        tagdict[dk] = tlist    
    return tagdict

def list_by_image():
    """
    build a dict of images and related tags
    """
    imgs = db(db.xim.id>0).select()
    imgdict = {}    
    for img in imgs:
        rows = (db(db.xref.xim==img.id).select())
        tlist = []
        for r in rows:
            tlist.append(r.xtg.name)
        # key is a tuple of image title and tag count        
        dk = (img.title,len(tlist))
        imgdict[dk] = tlist    
    return imgdict

def list_tag_summary():
    """
    built a list of tags and counts
    link to fn to retrieve related images    
    """
    imgdict = list_by_tag()
    #imgdict = list_by_image()
    dictlist =[]
    for k,v in imgdict.iteritems():
        ddnew = {}
        #ddnew['id'] =
        # unpack tuple
        kinfo, count = k
        id, name = kinfo
        #name = v
        ddnew['id'] = id
        ddnew['name'] = name
        ddnew['count'] = count
        # bug here -  need to return tag pk,  need to capture and save in dict
#        ddnew['name'] = A( XML(id), _href='/gaedemo/gaetagger/getbytag/%s' %id).xml()
        ddnew['link'] = A( XML(name), _href='/gaedemo/test/get_by_tag/%s' %id)
        #ddnew['link'] = A( XML(count), _href='/gaedemo/test/getbytag/%s' %id).xml()
        #ddnew['name'] = A( XML(id), _href='/gaedemo/gaetagger/getbytag/%s' %name)
        dictlist.append(ddnew)
    # return custom results
    return dict(tagsummary=dictlist)

def get_by_tag():
    """
    return list of images for the selected tag value 
    this is an ajax response - caller will expect json format
    """
    if not request.vars.search: return []
    tname = request.vars.search    
    if len(tname) < 2 : return []
    
    try:
        tg = db(db.xtg.name==tname).select().first()
    except:
        return ['No Matches Found']
    
    if not tg:   return ['No matches found']
    #tg_eu = db(db.xtg.name=='EU').select().first()
    rows = (db(db.xref.xtg==tg.id).select())
    #rows = (db(db.xref.xtg==tg.id).select()).as_list()
    imglist = []
    for r in rows:
        #imglist.append(r.xim.title)
        # build array here for proprt table rendering by 'TABLE'
        imglist.append([r.xim.title])

    #xmlstr =""
    #tbl = TABLE(TR(*rows) for rows in imglist).xml()
    tbl = TABLE(*[TR(*rows) for rows in imglist])
    return tbl

def get_by_name():
    """
    return list of images by title 
    (implement search like using gae)
    this is an ajax response - caller will expect json format
    """
    if not request.vars.search: return []
    tname = request.vars.search    
    if len(tname) > 2 : return []
    
    #rows = db(buyer.id>0).select().find(lambda row:row.name.startswith('C'))
    #rows = db(db.xim.id>0).select().find(lambda row:row.title.startswith(tname))
    
    rows = db(db.xim.id>0).select().find(lambda row:row.title.startswith(tname))
    
    #rows = db(db.xim.id>0).select()

    if not rows:   return ['No matches found']
    
    imglist = []
    for r in rows:
        #imglist.append(r.xim.title)
        # build array here for proprt table rendering by 'TABLE'
        # need to serve the blob as an image file
        # need to reformat the display here 
        #imglist.append([r.title, r.image])
        imglist.append([r.title, r.image_blob])

    #xmlstr =""
    #tbl = TABLE(TR(*rows) for rows in imglist).xml()
    tbl = TABLE(*[TR(*rows) for rows in imglist])
    return tbl
 
# crud form to edit an image 
def edit_image():
    id=request.args(0)
    return dict(form=crud.update(db.xim.id))

# add blob handling - after submit need to redirect to url
def add_image():

    url = URL('download')
    form = SQLFORM(db.xim, _name='xim_form',
            upload=url, 
            fields=['title', 'description', 'image'])

    #if request.vars.nprid:
        #form.vars.nprid = request.vars.nprid
    #if request.vars.title:
        #form.vars.title = request.vars.title
    #if request.vars.url:
        #form.vars.url = request.vars.url
    if request.vars.image != None:
        form.vars.image_filename = request.vars.image.filename

    if form.process().accepted:
        response.flash='record inserted'
        #xim_id = dict(form.vars)['id']
        #xim = db(db.xim.id==xim_id).select()
        redirect(URL(r=request, f='list_images'))

    elif form.errors: 
        response.flash='form errors'
    else:
        response.flash='complete form'
    return dict(form=form)

def list_images():
	#response.headers['Content-Type']='image/jpeg'
	# Display Image as jpeg file - need to set HTTP Content type = image/jpeg in view
	images=db(db.xim.id>0).select(orderby=db.xim.title)
	#response.headers['Content-Type']='image/jpeg' 

	#i8stream = images[8].image_blob
	#return response.stream(i8stream)
	#return i8stream
	return dict(images=images)

def list_blob_images():
    images=db(db.xim.id>0).select(orderby=db.xim.title)
    #return i8stream
    return dict(images=images)
    

# Modify handler to support blobstore
from gluon.settings import global_settings
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

import uuid
import logging

#modifications here to the gae handler to support gae blobstore
#web2py controller, handle gae blobstore upload
def upload_image():
	"""
	This is where an artist uploads a work of art.
	"""

	form = SQLFORM(db.xim, _name='xim_form',
			fields=['title', 'description', 'image'])

	if request.env.web2py_runtime_gae:
		from google.appengine.ext import blobstore
		import uuid
		#get the blob_info.  NOTE this MUST be done before any other operations on
		# the request vars.  otherwise something modifies them (perhaps the form
		# validators) in a way that makes this not work
		blob_info = None
		if request.vars.image != None:
			blob_info = blobstore.parse_blob_info(request.vars.image)

		upload_url = blobstore.create_upload_url(URL(r=request,f='upload_image',
													 args=request.args))

		form['_action']=upload_url
		if form.accepts(request.vars,session, formname="ximform"):
			#@TODO: can this blob-key update be a post-validation function?
			#get the record we just inserted/modified
			row = db(db.xim.id == form.vars.id).select().first()
			if request.vars.image__delete == 'on' or \
				(form.vars.image != None and (row and row.blob_key)):
				#remove from blobstore because of delete or update of image
				key = row.blob_key
				blobstore.delete(key)
				#remove reference in the xim record
				row.update_record(blob_key=None, image=None)
			if form.vars.image != None:
				#add reference to image in this record
				row.update_record(image = \
					"xim.image."+str(uuid.uuid4()).replace('-','')+".jpg",
					blob_key = blob_info.key())
			crud.archive(form)
			#Raise the HTTP exception so that the response content stays empty.
			#calling redirect puts content in the body which fails the blob upload
			raise HTTP(303,
					   Location= URL(r=request,f='list_blob_images'))
		elif form.errors:
			#logging.info("form not accepted")
			logging.info(form.errors)
			session.flash=BEAUTIFY(form.errors)
			#there was an error, let's delete the newly uploaded image
			if request.vars.image != None:
				blobstore.delete(blob_info.key())
			#Raise the HTTP exception so that the response content stays empty.
			#calling redirect puts content in the body which fails the blob upload
			raise HTTP(303,
					   Location= URL(r=request,f='upload_image'))

	return dict(form=form)

    
def download():

    #handle non-gae download
    if not request.env.web2py_runtime_gae or not request.args[0]:
        return response.download(request,db)

    #handle gae download
    #~ my_uploads=db(db.xim.preview_image==request.args[0]).select()[0]
    #my_uploads=db(db.xim.image==request.args[0]).select()[0]
    my_uploads=db(db.xim.id==request.args[0]).select()[0]
    if not my_uploads.blob_key:
        return None
    blob_info = blobstore.get(my_uploads.blob_key)

    response.headers['X-AppEngine-BlobKey'] = my_uploads.blob_key;
    response.headers['Content-Type'] = blob_info.content_type;
    response.headers['Content-Disposition'] = "attachment; filename=%s" % blob_info.filename
    return response.body.getvalue()

#----------------------------------------------------------------------
def show_image():
    """
    return image
    """
    
    if not request.args[0]:  return None
    id = request.args[0]
    response.headers['Content-Type']='image/jpeg'    
    #image=db(db.xim.id==25).select(orderby=db.xim.title).first()
    image=db(db.xim.id==id).select()    
    #return image
    return image[0].image_blob
    #return image[0].image

# custom form to upload to google blob engine
#@auth.requires_login()
def upload_xim():
    """
    This is where images are uploaded.
    """
    #~ form = SQLFORM(db.artwork,
                   #~ fields=['title',
                           #~ 'type',
                           #~ 'completed_date',
                           #~ 'image'])
                           
    url = URL('download')
    form = SQLFORM(db.xim, _name='xim_form',
            upload=url, 
            fields=['title', 'description', 'image'])
                           
    
    if request.env.web2py_runtime_gae:
          
        from google.appengine.ext import blobstore
        import uuid
        #get the blob_info.  NOTE this MUST be done before any other operations on
        # the request vars.  otherwise something modifies them (perhaps the form
        # validators) in a way that makes this not work
        blob_info = None
        if request.vars.image != None:
            blob_info = blobstore.parse_blob_info(request.vars.image)
      
        upload_url = blobstore.create_upload_url(URL(r=request,f='upload_xim',
                                                     args=request.args))
    
        form['_action']=upload_url
        if form.accepts(request.vars,session, formname="ximform"):
            #@TODO: can this blob-key update be a post-validation function?
            #get the record we just inserted/modified
            row = db(db.xim.id == form.vars.id).select().first()
            if request.vars.image__delete == 'on' or \
                (form.vars.image != None and (row and row.blob_key)):
                #remove from blobstore because of delete or update of image
                key = row.blob_key
                blobstore.delete(key)
                #remove reference in the artwork record
                row.update_record(blob_key=None, image=None)
            if form.vars.image != None:
                #add reference to image in this record
                row.update_record(image = \
                    "xim.image."+str(uuid.uuid4()).replace('-','')+".jpg",
                    blob_key = blob_info.key())
            crud.archive(form)
            #Raise the HTTP exception so that the response content stays empty.
            #calling redirect puts content in the body which fails the blob upload
            raise HTTP(303,
                       Location= URL(r=request,f='list_blob_images'))
   
    #~ if form.process().accepted:
        #~ response.flash='record inserted'
        #~ #xim_id = dict(form.vars)['id']
        #~ #xim = db(db.xim.id==xim_id).select()
        #~ redirect(URL(r=request, f='list_images'))                       
                       #~ 
        elif form.errors:
            #logging.info("form not accepted")
            logging.info(form.errors)
            session.flash=BEAUTIFY(form.errors)
            #there was an error, let's delete the newly uploaded image
            if request.vars.image != None:
                blobstore.delete(blob_info.key())
            #Raise the HTTP exception so that the response content stays empty.
            #calling redirect puts content in the body which fails the blob upload
            raise HTTP(303,
                       Location= URL(r=request,f='upload_image'))
    
    return dict(form=form)    


    

