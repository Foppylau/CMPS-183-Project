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
                Field('circle', requires=IS_IN_SET(['Housemates', 'Events', 'Individual loans', 'Subscriptions'])),
                Field('price', 'decimal(7,2)'),
                Field('status', requires=IS_IN_SET(['Pay', 'Pending', 'Confirmed']))
                )

db.define_table('pictures',
                Field('user_email', default=auth.user.email if auth.user_id else None, readable = False),
                Field('file_name', 'upload')
                )


db.pictures.user_email.readable = False
db.pictures.user_email.writable = False
#db.pictures.user_email.requires = IS_NOT_IN_DB(db, db.pictures.user_email)

db.define_table('item',
                Field('bill_name', 'text'),
                Field('item_name', 'text'),
                Field('creator', default=auth.user.email if auth.user_id else None),
                Field('contributors', 'text',default=None),
                Field('price', 'decimal(7,2)'),
                Field('status', requires=IS_IN_SET(['Unpaid', 'Payment Pending', 'Payment Received']))
                )

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
