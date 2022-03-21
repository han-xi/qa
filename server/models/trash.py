from email.policy import default
from enum import unique
from run import db
import datetime
class Trash(db.Document):
    meta = {
        'collection': 'trash',
        # 'ordering': [''],
        'strict': False,
    }
    class_id = db.StringField(required=True)
    user_id = db.StringField(required=True)
    ispushmsg = db.BooleanField(default=False)
    insert_type=db.StringField(required=True)
    inserttime = db.DateTimeField(default=datetime.datetime.now)
class TrashUser(db.Document):
    meta = {
        'collection': 'trashuser',
        # 'ordering': [''],
        'strict': False,
    }
    user_id = db.StringField(required=True)
    user_type = db.IntField(required=True)
    ispushmsg = db.BooleanField(default=False)
    insert_type=db.StringField(required=True)
    inserttime = db.DateTimeField(default=datetime.datetime.now)
    insertname = db.StringField(required=True)