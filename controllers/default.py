# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    logged_in = auth.user_id is not None
    if(logged_in):
        redirect(URL('default', 'newsfeed'))
    return dict(logged_in=logged_in, message=T('Welcome to PayMe!'))

def settings():
    grid = SQLFORM(db.pictures, ignore_rw=True, deletable=True)
    if grid.process().accepted:
        response.flash = 'form accepted'
    elif grid.errors:
        response.flash = 'form has errors'

    row = db(db.pictures.user_email == auth.user.email).select().first()
    if row is not None:
        picture = row.file_name
    else:
        picture = "slug.png"


    return dict(grid = grid, profile_pic = picture)


def housemate():
    row = db(db.pictures.user_email == "default@ucsc.edu").select().first()
    picture = row.file_name
    if auth.user is not None:
        row = db(db.pictures.user_email == auth.user.email).select().first()
        if row is not None:
            picture = row.file_name

    logged_in = auth.user_id is not None

    if(not logged_in):
        redirect(URL('default', 'user'))

    return dict(profile_pic=picture,logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)

def events():
    logged_in = auth.user_id is not None
    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)
def individual_loans():
    logged_in = auth.user_id is not None
    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)
def subscriptions():
    logged_in = auth.user_id is not None
    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)
def newsfeed():
    logged_in = auth.user_id is not None
    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


