# -*- coding: utf-8 -*-
#
# gaetagger tag controller
#
#########################################################################
## This is a tag controller which works with GAE models
## - handle all tag related actions
## - build tag list
#########################################################################

import datetime

def list_tag_summary():
    """ 
    Use map table to list image tags
    Build a dict of names and counts
    """
    # init list of tags and names
    tags = db(db.tag.id>0).select()
    dtags ={}
    for row in tags:
        dtags[row.id] = row.name        
    # Sort images by tag_id    
    
    imgtags=db(db.imagetag.id>0).select(orderby=db.imagetag.tag_id)
    #imgtags=db(db.imagetag.id>0).select(orderby=db.imagetag.tag_id).as_dict
    # retrieve 'as_dict' for easier group by 
    rdict = {}
    taglist =[]
    for row in imgtags:
        # break on change of id
        #tag =  db(db.tag.id==row.tag_id).select().first()
        tagname = dtags[int(row.tag_id)]
        if tagname in rdict.keys():
            rdict[tagname] += 1
        else:
            rdict[tagname] = 1
    return rdict
        
        #if row.tag_id != tagid:
            #if tagid >0:
                #rdict[tag.name] = tagcnt
            #tagid = row.tag_id
            ## get the tagname
            #tag =  db(db.tag.id==row.tag_id).select().first()
            #tagname = tag.name
            #tagcnt = 1
        #else:    
            ##tagid = row.tag_id
            #tagcnt += 1
    ## don't forget the last one
    #rdict[tagname] = tagcnt
    #return rdict

def gettagsummary():
    """
    Get list of tags and related counts (from imagetag table) - user can then view by tag
    (similar to Stack Overflow tag view??) 
    """
    count = db.imagetag.tag.count()
    tagsummary = db(db.imagetag.tag==db.tag.id).select(
        db.imagetag.tag, db.tag.name, count, \
        groupby=db.imagetag.tag)
    
    # build custom list of dicts here  
    tlist = []
    for item in tagsummary:                
        d = {}
        tagid = item.imagetag.tag
        name = item.tag.name
        d['count'] = item[count]    # <-- note the syntax
        #d['name'] = item.tag.name
        d['name'] = A( XML(name), _href='/gaedemo/gaetagger/getbytag/%s' %tagid).xml()        
        #d['name'] = A( XML(name), _href='/gallery/default/getbytag/%s' %tagid).xml()        
        d['id'] = tagid
        tlist.append(d)

    # return custom results
    return dict(tagsummary=tlist)

def getbytag():
    """
        Return detail list of images matching selected tag
    """ 
    if  request.args(0):
        tagval = request.args(0)
        #queries with %LIKE% ****HERE BE THE DRAGONS!!!!******
        images = db(db.imagetag.tag==db.tag.id)(db.tag.id==tagval)(db.image.id==db.imagetag.image).select(db.image.ALL)
    else:
        images = db(db.image.ALL).select()

    s = "<ul id='albumlist'>"
    for r in images:
        print  s
        s += LI(IMG(_src=URL('default','download', args= r.file), _width="120", _height="100"  ), A(r.title, _href=URL('default','show',args=r.id))).xml()
    s += "</UL>"
    response.view = 'gaetagger/tagmatches.html'
    return dict(images=images)


def list_all_tags():
    #~ tags=db(db.tag.created_by==auth.user_id).select(orderby=db.tag.title)
    tags=db(db.tag.id>0).select(orderby=db.tag.name)
    return dict(tags=tags)

def list_image_tags():
    """ Use map table to list image tags and related counters """
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

def list_img_tags():
    '''
    Build dict of tags for an image - request is an ajax request
    see: https://groups.google.com/forum/#!searchin/web2py/tag$20examples/web2py/j7Gy5gmf1EY/crQnrLzAooYJ
    '''
    query = db.image.id>0
    tags_d = db(db.tag.id>0).select(cache=(cache.ram,600)).as_dict()
    image_d = db(query).select().as_dict()
    # remove for gae
    #links = db(db.tag.image.belongs(image_d.keys())).select()
    rows=[]
    for link in links:
        if rows and rows[-1][0].id==link.tag.image:
            tags=rows[-1][1]
        else:
            tags=[]
            rows.append((image_d[link.tag.image],tags))
        if link.tag.tag: tags.append(tags_d[link.tag.tag])

    for row in rows:
        print 'image object:', row[0], 'list of tags', row[1]
    return ""
