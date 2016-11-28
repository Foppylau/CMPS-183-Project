import random

def index():
    pass

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


# Mocks implementation.
def get_posts():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    # We just generate a lot of of data.
    posts = []
    has_more = False
    rows = db().select(db.post.ALL, limitby=(start_idx, end_idx + 1), orderby=~db.post.created_on)



    for i, r in enumerate(rows):
        if i < end_idx - start_idx:

            if auth.user_id is not None and r.user_email == auth.user.email:
                mypost = True
            else:
                mypost = False

            t = dict(
                id = r.id,
                post_content = r.post_content,
                user_email = get_user_name_from_email(r.user_email),
                created_on = r.created_on,
                updated_on = r.updated_on,
                creator = r.creator,
                circle = r.circle,
                bill = r.bill,
                payer = r.payer,
                price = r.price,
                status = r.status,
                mypost = mypost
            )
            posts.append(t)
        else:
            has_more = True
    logged_in = auth.user_id is not None
    print(auth.user.email)

    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,

    ))

@auth.requires_signature()
def add_post():
    t_id = db.post.insert(
        post_content = request.vars.post_content,
        creator = request.vars.creator,
        circle = request.vars.circle,
        bill = request.vars.bill,
        payer = request.vars.payer,
        price = request.vars.price,
        status = request.vars.status
    )
    t = db.post(t_id)
    return response.json(dict(post=t))

@auth.requires_signature()
def del_post():
    db(db.post.id == request.vars.post_id).delete()
    return "ok"


@auth.requires_signature()
def edit_post():
    t_id = request.vars.post_id
    row = db(db.post.id == t_id).select().first()
    print(request.vars.edit_content)
    row.update_record(post_content=request.vars.edit_content)

def update_post():
    """Here we get edits to a post and update the database"""

    #This check prevents empty updates from being submitted
    if request.vars.edit_content != "":
        p = db.post(request.vars.post_id)
        p.post_content = request.vars.edit_content
        p.updated_on = datetime.datetime.utcnow()
        p.update_record()
        response.flash = T("Post Updated")
        return response.json(dict(post=p, idx = False))
    else:
        response.flash = T("Post Cannot Be Empty")
        return response.json(dict(idx=True))

# def update_post():
#     """Here we get edits to a post and update the database"""
#
#     #This check prevents empty updates from being submitted
#     if request.vars.edit_content != "":
#         p = db.post(request.vars.post_id)
#         p.post_content = request.vars.edit_content
#         p.updated_on = datetime.datetime.utcnow()
#         p.update_record()
#         response.flash = T("Post Updated")
#         return response.json(dict(post=p, idx = False))
#     else:
#         response.flash = T("Post Cannot Be Empty")
#         return response.json(dict(idx=True))

# @auth.requires_signature()
# def edit_post():
#     db(db.post.post_content == request.vars.edit).update()
#     return response.json(dict(post=t))
