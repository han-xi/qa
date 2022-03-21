from email.policy import default
from run import db
from flask import current_app
from passlib.hash import pbkdf2_sha256 as sha256
import datetime
class UserType():
    student = 1
    tearcher = 2
    admin = 3
class User(db.Document):
    meta = {
        'collection': 'user',
        # 'ordering': [''],
        'strict': False,
    }
    # id = db.StringField(required=True)
    username =  db.StringField(required=True, max_length=128, unique=True)
    password =  db.StringField(required=True, max_length=128)
    registertime = db.DateTimeField(default=datetime.datetime.now)
    usertype = db.IntField(default=1)    
    activate = db.BooleanField(default=False)
    activatetime= db.DateTimeField()
    activatename = db.StringField()
    islogin = db.BooleanField(default=False)
    isupgrade = db.BooleanField(default=False)
    upgradetime = db.DateTimeField()
class RegisterUser(db.Document):
    meta = {
        'collection': 'registeruser',
        # 'ordering': [''],
        'strict': False,
    }
    username =  db.StringField(required=True, max_length=128, unique=True)
    password =  db.StringField(required=True, max_length=128)
    registertime = db.DateTimeField(default=datetime.datetime.now)   
    code = db.StringField()
    isactivate = db.BooleanField(default=False)
    activatetime= db.DateTimeField()
class ForgetUser(db.Document):
    meta = {
        'collection': 'forgetuser',
        # 'ordering': [''],
        'strict': False,
    }
    username =  db.StringField(required=True, max_length=128, unique=True)
    password =  db.StringField(required=True, max_length=128)
    registertime = db.DateTimeField(default=datetime.datetime.now)   
    code = db.StringField()
    isactivate = db.BooleanField(default=False)
    activatetime= db.DateTimeField()
