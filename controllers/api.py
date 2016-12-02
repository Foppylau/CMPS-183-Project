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
    items = []
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
                circle = r.circle,
                price = r.price,
                status = r.status,
                mypost = mypost
            )
            posts.append(t)
        else:
            has_more = True

    item_rows = db().select(db.item.ALL)
    for i, r in enumerate(item_rows):
        t = dict(
            id = r.id,
            bill_name = r.bill_name,
            item_name = r.item_name,
            creator = r.creator,
            contributors = r.contributors,
            price = r.price,
            status = r.status
        )
        items.append(t)


    logged_in = auth.user_id is not None
    print(auth.user_id)

    return response.json(dict(
        posts=posts,
        items=items,
        logged_in=logged_in,
        has_more=has_more,

    ))

@auth.requires_signature()
def add_post():
    t_id = db.post.insert(
        post_content = request.vars.post_content,
        circle = request.vars.circle,
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
def del_item():
    db(db.item.id == request.vars.item_id).delete()
    return "ok"


@auth.requires_signature()
def edit_post():
    t_id = request.vars.post_id
    row = db(db.item.id == t_id).select(db.item.contributors)
    row.update_record(post_content=request.vars.edit_content)
    return "ok"


@auth.requires_signature()
def add_contributer():
    t_id = request.vars.item_id
    row = db(db.item.id == t_id).select().first()
    print(row)
    row.update_record(contributors=auth.user.email)
    return "ok"

@auth.requires_signature()
def add_item():
    t_id = db.item.insert(
        bill_name = request.vars.bill_name,
        item_name = request.vars.item_name,
        price = request.vars.price
    )
    t = db.item(t_id)
    return response.json(dict(item=t))


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
