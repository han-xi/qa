from email.policy import default
from enum import unique
from threading import local

from numpy import require
from run import db
import datetime
class Class(db.Document):
    meta = {
        'collection': 'class',
        # 'ordering': [''],
        # 'auto_create_index':False,
        'strict': False,
    }
    # id = db.ObjectIdField()
    classname =  db.StringField(required=True, max_length=128, unique=True)
    problems = db.ListField(db.StringField())
    registertime = db.DateTimeField(default=datetime.datetime.now)
    updatetime = db.DateTimeField(default=datetime.datetime.now)
    insertname = db.StringField()
    limitnum = db.IntField(default=50)
    status = db.IntField(default = 1)
    content = db.StringField()
    starttime = db.DateTimeField(required=True)
    endtime =  db.DateTimeField(required=True)
class ClassStudent(db.Document):
    meta = {
        'collection': 'classstudent',
        # 'ordering': [''],
        'strict': False,
    }      
    class_id = db.StringField(required=True)
    student_id =db.StringField(required=True)
    insertname = db.StringField(required=True)
    activate = db.BooleanField(default=False)
    activatename = db.StringField()
    activatetime = db.DateTimeField()
    updatetime = db.DateTimeField(default=datetime.datetime.now)
    ispushmsg = db.BooleanField(default=False)
class ClassTeacher(db.Document):
    meta = {
        'collection': 'classteacher',
        # 'ordering': [''],
        'strict': False,
    }      
    class_id = db.StringField(required=True)
    teacher_id =db.StringField(required=True)
    insertname = db.StringField(required=True)
    activate = db.BooleanField(default=False)
    activatename = db.StringField()
    activatetime = db.DateTimeField()
    updatetime = db.DateTimeField(default=datetime.datetime.now)
    ispushmsg = db.BooleanField(default=False)
