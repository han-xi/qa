from flask import Flask
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flask_mail import Mail
app = Flask(__name__)
api = Api(app)
CORS(app)

app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "1179865214@qq.com"
app.config["MAIL_PASSWORD"] = "gqlvlmkmyvczgfhj"
app.config["MAIL_DEFAULT_SENDER"] = "1179865214@qq.com"

app.config["TOKEN_EXPIRATION"] =3600 #一小时
app.config['SECRET_KEY'] = 'hello@#$%&'
mail=Mail(app)
app.config['MONGODB_SETTINGS']={
        'db': 'test',
        'host': 'localhost',
        'port': 27017,
        'connect': True,
        # 'username': 'test',
        # 'password': '123456',
        # 'authentication_source': 'admin'
}
from datetime import timedelta
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['JWT_SECRET_KEY'] = 'hello@#$%&'
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['DEBUG'] = True
# db = SQLAlchemy(app)
db = MongoEngine(app)
# db.init_app(app)
# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWTManager(app)

from models import user,classes,question
from resources import userResources,classResources,questionResources
api.add_resource(userResources.UserRegistration, '/register')
api.add_resource(userResources.UserForget,'/forgetpassword')
api.add_resource(userResources.ForgetActivate,'/forgetactivate')
api.add_resource(userResources.Activate,'/activate')
api.add_resource(userResources.UserLogin, '/login')
api.add_resource(userResources.GetImagecode,'/getcode')
api.add_resource(userResources.SecretResource, '/home')
api.add_resource(userResources.TokenRefresh, '/token/refresh')
api.add_resource(userResources.UpgradePermissionResource,'/upgradepermission')
api.add_resource(userResources.getUpgradePermissionListResource,'/getupgradepermissionlist')
api.add_resource(userResources.AddUpgradePermissionListResource,'/addupgradepermission')
api.add_resource(userResources.DeleteUpgradePermissionListResource,'/deleteupgradepermission')

api.add_resource(classResources.GetClassResource, '/classinfo')
api.add_resource(classResources.PostClassResource,'/postclassinfo')
api.add_resource(classResources.GetClassListResource, '/classlist')
api.add_resource(classResources.AddClassResource, '/addclass')
api.add_resource(classResources.DeleteClassResource, '/deleteclass')
api.add_resource(classResources.GetStudentResource, '/studentinfo')
api.add_resource(classResources.GetTeacherResource,'/teacherinfo')
api.add_resource(classResources.GetStudentListResource, '/studentlist')
api.add_resource(classResources.AddStudentResource,'/addstudent')
api.add_resource(classResources.AddTeacherResource,'/addteacher')
api.add_resource(classResources.GetApplyStudentListResource,'/getapplystudentlist')
api.add_resource(classResources.GetApplyTeacherListResource,'/getapplyteacherlist')
api.add_resource(classResources.ApplyStudentResource,'/applystudent')
api.add_resource(classResources.ApplyTeacherResource,'/applyteacher')
api.add_resource(classResources.DeleteStudentResource,'/deletestudent')
api.add_resource(classResources.DeleteTeacherResource,'/deleteteacher')
api.add_resource(classResources.GetMesageCountResource,'/getmessagecount')
api.add_resource(classResources.GetMessageInfoResource,'/getmessageinfo')

api.add_resource(questionResources.GetQuestionResource,'/questioninfo')
api.add_resource(questionResources.GetQuestionListResource,'/questionlist')
api.add_resource(questionResources.AddQuestionResource,'/addquestion')
api.add_resource(questionResources.GetWrongQuestionResource,'/wronginfo')
api.add_resource(questionResources.GetWrongQuestionListResource,'/wronglist')
api.add_resource(questionResources.GetWrongQuestionListResourceForHome,'/wronglistforhome')
api.add_resource(questionResources.GetWrongQuestionListResourceByUserid,'/wronglistbyuserid')
api.add_resource(questionResources.AddWrongQuestionResource,'/addwrong')
api.add_resource(questionResources.DeleteWrongQuestionResource,'/deletewrong')
api.add_resource(questionResources.GetCollectQuestionResource,'/collectlist')
api.add_resource(questionResources.AddCollectQuestionResource,'/addcollect')
api.add_resource(questionResources.DeleteCollectQuestionResource,'/deletecollect')


api.add_resource(userResources.Test,'/test')



@app.after_request
def after(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods']='POST,GET,OPTIONS,DELETE,HEAD,PUT,PATCH'
    response.headers['Content-Type']='application/json;application/x-www-form-urlencoded;image/gif;image/png;image/jpeg'
    return response
if __name__=="__main__":
    app.run(debug=True)