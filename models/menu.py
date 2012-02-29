# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

# -*- coding: utf-8 -*- 

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

# response.title = request.application
response.title = T('GAE Demo App!')
response.subtitle = T('Many to Many Test')

##########################################
## this is the main application menu
## add/remove items as required
##########################################
response.menu = [
    ['Home', False, URL(request.application,'default','index')],
    
    (T('Tags'), False, URL('default','index'), [
    
    (T('My Tags'), False, URL(request.application,'default','list_tags'),[]),
    (T('Add Tag'), False, URL(request.application,'default','add_tag'),[]),
    (T('My Images'), False, URL(request.application,'default','list_images'),[]),
    (T('Add Image'), False, URL(request.application,'default','add_image'),[],
    ),        
    ]),            
        

    (T('Show'), False, URL('default','index'), [
        (T('Show By Tag'), False, URL('default','list_by_tag'), []),            
        (T('Show By ImgTag'), False, URL('default','list_by_image_imagetag'), []),
        (T('Show By Image'), False, URL('default','list_by_image'), []),
        (T('Tag Summary'), False, URL('test','list_tag_summary'), [],
        ),        
    ]),            

    (T('Test'), False, URL('default','index'), [
        (T('List Blob Images'), False, URL('test','list_blob_images'), []),            
        (T('Add Blob Image'), False, URL('test','upload_image'), []),
        #(T('Add Blob Image'), False, URL('test','upload_xim'), []),
        (T('Add Image'), False, URL('test','add_image'), []
        ),        
    ]),            
    ]

