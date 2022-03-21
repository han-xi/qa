from email.policy import default
from run import db
import datetime
from bson.objectid import ObjectId
class Question(db.Document):
    meta = {
        'collection': 'question',
        # 'ordering': [''],
        'strict': False,
    }
    # id = db.StringField()
    problem =  db.StringField(required=True)
    options = db.ListField(db.StringField())
    answer = db.IntField()
    tag = db.ListField(db.StringField(max_length=30))
    class_id = db.ListField(db.StringField())
    score = db.FloatField(default = 0.0)
    updatetime = db.DateTimeField(default=datetime.datetime.now)
    insertname = db.StringField()

class WrongQuestion(db.Document):
    meta = {
        'collection': 'wrongquestion',
        # 'ordering': [''],
        'strict': False,
    }
    # id = db.StringField(required=True)
    problem_id =  db.StringField(required=True)
    user_id = db.StringField(required=True)
    wrong_answer = db.StringField(required=True)
    num = db.IntField(default=1)
    updatetime = db.DateTimeField(default=datetime.datetime.now)
class CollectQuestion(db.Document):
    meta = {
        'collection': 'collectquestion',
        # 'ordering': [''],
        'strict': False,
    }
    # id = db.StringField(required=True)
    problem_id =  db.StringField(required=True)
    user_id = db.StringField(required=True)
    updatetime = db.DateTimeField(default=datetime.datetime.now)   
