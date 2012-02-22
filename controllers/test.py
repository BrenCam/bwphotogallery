# test controller for gae join

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

#----------------------------------------------------------------------
def list_tagsummary():
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
        ddnew['link'] = A( XML(count), _href='/gaedemo/gaetagger/getbytag/%s' %id).xml()
        #ddnew['name'] = A( XML(id), _href='/gaedemo/gaetagger/getbytag/%s' %name)
        dictlist.append(ddnew)
    # return custom results
    return dict(tagsummary=dictlist)