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

def get_totals():
    # get total owed by you to others
    total_owes = 0

    items = db().select(db.item.ALL)
    for item in items:
        payers = item.contributors

        if payers is None:
            continue
        payers = payers.split()
        print(payers)
        number_of_payers = len(payers)
        if (auth.user.email in payers):
            total_owes += (item.price / number_of_payers)

    # get total owed by others to you
    total_owed = 0
    new_items = db().select(db.item.ALL)
    for item in new_items:
        creator = item.creator

        if creator is None:
            continue

        print(creator)
        print("yo!")
        if (auth.user.email == creator):
            total_owed += item.price

    print(total_owed)
    totals = []
    totals.append(total_owed)
    totals.append(total_owes)
    return(totals)

def get_picture():
    picture = None
    if auth.user is not None:
        row = db(db.pictures.user_email == auth.user.email).select().last()
        if row is not None:
            picture = row.file_name

    if picture is None:
        d = 'default'
        row = db(db.pictures.user_email == 'default@default.com').select().first()
        if row is not None:
            picture = row.file_name
    return picture

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

def housemate():
    logged_in = auth.user_id is not None
    if (not logged_in):
        redirect(URL('default', 'user'))
    picture = get_picture()

    totals = get_totals()
    total_owed = totals[0]
    total_owes = totals[1]

    return dict(profile_pic=picture, logged_in=logged_in, get_user_name_from_email=get_user_name_from_email, total_owes=total_owes, total_owed=total_owed)

def events():
    picture = None
    if auth.user is not None:
        row = db(db.pictures.user_email == auth.user.email).select().first()
        if row is not None:
            picture = row.file_name

    logged_in = auth.user_id is not None

    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(profile_pic=picture, logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)

def individual_loans():
    picture = None
    if auth.user is not None:
        row = db(db.pictures.user_email == auth.user.email).select().first()
        if row is not None:
            picture = row.file_name

    logged_in = auth.user_id is not None

    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(profile_pic=picture, logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)

def subscriptions():
    picture = None
    if auth.user is not None:
        row = db(db.pictures.user_email == auth.user.email).select().first()
        if row is not None:
            picture = row.file_name

    logged_in = auth.user_id is not None

    if picture is None:
        d = 'default'
        row = db(db.pictures.user_email == 'default@default.com').select().first()
        if row is not None:
            picture = row.file_name

    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(profile_pic=picture, logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)

def newsfeed():
    picture = None
    if auth.user is not None:
        row = db(db.pictures.user_email == auth.user.email).select().first()
        if row is not None:
            picture = row.file_name

    logged_in = auth.user_id is not None

    if (not logged_in):
        redirect(URL('default', 'user'))

    return dict(profile_pic=picture, logged_in=logged_in, get_user_name_from_email=get_user_name_from_email)

def settings():
    grid = SQLFORM(db.pictures, deletable=True)
    if grid.process().accepted:
        response.flash = 'form accepted'
        redirect(URL('default', 'newsfeed'))
    elif grid.errors:
        response.flash = 'form has errors'
    

    return dict(grid = grid)

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


