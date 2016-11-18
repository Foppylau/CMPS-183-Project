# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

def get_user_email():
    return auth.user.email if auth.user else None

db.define_table('post',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('post_content', 'text'),
                Field('created_on', 'datetime', default=datetime.datetime.today()),
                Field('updated_on', 'datetime', update=datetime.datetime.today()),
                Field('creator', default=auth.user.email if auth.user_id else None),
                Field('payer', 'text',default=None),
                Field('circle', requires=IS_IN_SET(['Housemates', 'Events', 'Individual loans', 'Subscriptions'])),
                Field('bill', 'text'),
                Field('price', 'decimal(7,2)'),
                Field('status', requires=IS_IN_SET(['Pay', 'Pending', 'Confirmed']))
                )



# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
