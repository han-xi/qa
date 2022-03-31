
from flask_restful import Resource, reqparse
from models.user import User,RegisterUser,ForgetUser
from models.trash import TrashUser
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from datetime import date, datetime
from flask import jsonify,request,make_response
from io import BytesIO

from util.send_mail import send_mail,validateEmail,check_activate_token,generate_activate_token,md5,validate_picture,check_activate_token_forever,generate_activate_token_forever
import base64
import re
parser = reqparse.RequestParser()
parser.add_argument(
    'username', help='This field cannot be blank')
parser.add_argument(
    'password', help='This field cannot be blank')
parser.add_argument(
    'usertype', required=False)
parser.add_argument(
    'code', required=False)
parser.add_argument(
    'check_code', required=False)

parser.add_argument(
    'current', required=False)
parser.add_argument(
    'search', required=False)
parser.add_argument(
    'search1', required=False)

parser.add_argument(
    'sorter', required=False)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        isok = validateEmail(data['username'])

        if isok :
            check_code = check_activate_token_forever(data["check_code"]).get('id') 
            print(check_code,data['code'])
            if check_code and check_code == data['code']:
                if User.objects(username = data['username']).first():
                    return {'message': '用户 {} already exists'.format(data['username'])}
                newregister = RegisterUser.objects(username = data['username']).first()
                if newregister:
                    token = str(generate_activate_token(data['username']),'utf-8')
                    newregister.update(code=token,password = md5(data['password']))
                    send_mail(data['username'],token)
                    return {'message': '用户 {} 的注册激活码已刷新，请查收邮件'.format(data['username'])}
                token = str(generate_activate_token(data['username']),'utf-8')
                new_user = RegisterUser(
                    username=data['username'],
                    password=md5(data['password']),
                    code = token
                )
                try:
                    new_user.save()
                    # access_token = create_access_token(identity={'user':data['username']})
                    send_mail(data['username'],token)
                    
                    # refresh_token = create_refresh_token(identity={'user':data['username']})
                    response_object = {
                        'message': '用户 {} 注册申请已收到，请到邮箱激活账户，激活码有效期1小时'.format(data['username']),
                        # 'access_token': access_token,
                        # 'refresh_token': refresh_token
                    }
                except:
                    response_object = {'message': 'Something went wrong'}, 500
            else:
                response_object = {'message': '验证码输入错误'},400
               
            return response_object
        else:
            return {'message':'输出格式错误'},400
class UserForget(Resource):
    def post(self):
        data = parser.parse_args()
        isok = validateEmail(data['username'])

        if isok :
            check_code = check_activate_token_forever(data["check_code"]).get('id') 
            print(check_code,data['code'])
            if check_code and check_code == data['code']:
                if User.objects(username = data['username']).count==0:
                    return {'message': '用户 {} 不存在'.format(data['username'])}
                newregister = ForgetUser.objects(username = data['username']).first()
                if newregister:
                    token = str(generate_activate_token(data['username']),'utf-8')
                    newregister.update(code=token,password = md5(data['password']))
                    send_mail(data['username'],token,send_type='forget')
                    return {'message': '用户 {} 的更改密码激活码已刷新，请查收邮件'.format(data['username'])}
                token = str(generate_activate_token(data['username']),'utf-8')
                new_user = ForgetUser(
                    username=data['username'],
                    password=md5(data['password']),
                    code = token
                )
                try:
                    new_user.save()
                    # access_token = create_access_token(identity={'user':data['username']})
                    send_mail(data['username'],token,send_type='forget')
                    
                    # refresh_token = create_refresh_token(identity={'user':data['username']})
                    response_object = {
                        'message': '用户 {} 修改密码申请已收到，请到邮箱激活账户，激活码有效期1小时'.format(data['username']),
                        # 'access_token': access_token,
                        # 'refresh_token': refresh_token
                    }
                except:
                    response_object = {'message': 'Something went wrong'}, 500
            else:
                response_object = {'message': '验证码输入错误'},400
               
            return response_object
        else:
            return {'message':'输出格式错误'},400
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        isok = validateEmail(data['username'])
        if isok:
            check_code = check_activate_token_forever(data["check_code"]).get('id')
            print(check_code,data['code'])
            if check_code and check_code == data['code']:
                current_user = User.objects(username=data['username']).first()
                if not current_user:
                    return {'message': 'User {} doesn\'t exist'.format(data['username'])}
                if md5(data['password']) ==current_user.password:
                    access_token = create_access_token(identity={'user':data['username']},fresh=True)
                    refresh_token = create_refresh_token(identity={'user':data['username']})
                    return {
                        'message': 'Logged in as {}'.format(current_user.username),
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'username':data['username'],
                        'usertype':current_user.usertype
                    }
                else:
                    return {'message': '密码错误'},403
            else:
                return {'message':'验证码输入错误'},400
        else:
            return {'message':'输出格式错误'},400

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def put(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user,fresh=False)
        return {'access_token': access_token}

class Activate(Resource):
    def get(self):
        check_token = request.args.get("token")
        if check_token:
            data = check_activate_token(check_token)
            if data:
                user = User.objects(username= data['id']).first()
                register_user = RegisterUser.objects(username = data['id'],code =check_token ).first()
                if user:
                    return {'message':'用户已存在'},403
                elif register_user:
                    newUser = User(username = data['id'],password =register_user.password)
                    try:
                        newUser.save()
                        return {
                            'message':'成功激活'
                        }
                    except:
                        return {'message':'系统错误'},500
                else:
                    return {'message':'激活码错误,请返回注册页面重新申请激活码'},403
            else:
                return {'message':'激活码错误,请返回注册页面重新申请激活码'},400
            
        return {
            'message':'token错误'
        }
class ForgetActivate(Resource):
    def get(self):
        check_token = request.args.get("token")
        if check_token:
            data = check_activate_token(check_token)
            if data:
                user = User.objects(username= data['id']).first()
                register_user = ForgetUser.objects(username = data['id'],code =check_token ).first()
                if user==None:
                    return {'message':'用户不存在'},403
                elif register_user:            
                    try:
                        user.update(password =register_user.password)
                        return {
                            'message':'成功激活'
                        }
                    except:
                        return {'message':'系统错误'},500
                else:
                    return {'message':'激活码错误,请返回忘记密码页面重新申请激活码'},403
            else:
                return {'message':'激活码错误,请返回忘记密码页面重新申请激活码'},400
            
        return {
            'message':'token错误'
        }

class SecretResource(Resource):
    @jwt_required()
    def get(self):
        userIdentity = get_jwt_identity()
        print(userIdentity)
        current_user = User.objects(username = userIdentity['user']).first()
        return {
            'username': '{}'.format(current_user.username),
            'registertime': '{}'.format(current_user.registertime.strftime("%Y-%m-%d %H:%M:%S")),
            'usertype': '{}'.format(current_user.usertype),
            'activate': '{}'.format(current_user.activate),
        }, 200
class UpgradePermissionResource(Resource):
    @jwt_required()
    def post(self):
        userIdentity = get_jwt_identity()
        current_user = User.objects(username = userIdentity['user']).first()
        if current_user:
            try:
                current_user.update(isupgrade=True,upgradetime= datetime.now)
                return {'message':'审核中，请耐心等待'}
            except:
                return {'message':'something wrong'},500
        return  {'message':'未授权'},403
class getUpgradePermissionListResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        usertype_dict = {
            2:'教师',
            3:'管理员'
        }
        if data['search1']!='':
            if data['search1']=='管理员':
                data['search1']=2
            elif data['search1']=='教师':
                data['search1']=1
            else:
                data['search1']=''
        current_user = User.objects(username = userIdentity['user']).first()
        if current_user and current_user.usertype>2:
            if data['search']!='' and data['search1']!='':
                regex = re.compile('.*'+data['search']+'.*')
                current_apply = User.objects(isupgrade=True,username=regex,usertype=data['search1']).all()
            elif data['search']!='':
                regex = re.compile('.*'+data['search']+'.*')
                current_apply = User.objects(isupgrade=True,username=regex).all() 
            elif data['search1']!='':
                current_apply = User.objects(isupgrade=True,usertype=data['search1']).all()                            
            else:
                current_apply = User.objects(isupgrade=True).all()
            if data['sorter']=='ascend':
                current_apply =current_apply.order_by('upgradetime').paginate(
                page=int(data['current']), per_page=5).items  
            elif data['sorter'] =='descend':
                current_apply=current_apply.order_by('-upgradetime').paginate(
                page=int(data['current']), per_page=5).items  
            else:
                current_apply=current_apply.paginate(
                page=int(data['current']), per_page=5).items                
            total = len(current_apply)
            for item in current_apply:
                result.append({
                    'username':item.username,
                    'usertype':usertype_dict[item.usertype+1],
                    'updatetime':'{}'.format(item.upgradetime.strftime("%Y-%m-%d %H:%M:%S")),
                    'key':item.username,
                    'isoperated':False
                })
            return {'result':result,'total':total}
        return  {'result':result,'total':0}
class AddUpgradePermissionListResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        current_user = User.objects(username = userIdentity['user']).first()
        if current_user and current_user.usertype>2:
            current_user = User.objects(username = data['username']).first()
            if current_user.isupgrade ==False:
                return {'message':'请勿重复提交请求'}
            try:
                usertype = current_user.usertype
                current_user.update(isupgrade=False,usertype = current_user.usertype+1,upgradetime= datetime.now)
                newTrashUser = TrashUser(user_id = data['username'],user_type=usertype+1,insert_type = 'admit')
                newTrashUser.save()
                return {'message':'升级成功'}
            except:
                return {'message':'something wrong'},500
        
        return {'message':'无权限'},403
class DeleteUpgradePermissionListResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user = User.objects(username =userIdentity['user']).first()
        if user and user.usertype>2:
            try:
                current_user = User.objects(username =data['username']).first()
                current_user.update(isupgrade=False)
                newTrashUser = TrashUser(user_id = data['username'],user_type=current_user.usertype+1,insert_type = 'notadmit',insertname=userIdentity['user'])
                newTrashUser.save()
                return {'message':'驳回成功'}
            except:
                return {'message':'something wrong'},500
        return {'message':'无权限'},403
class Test(Resource):
    @jwt_required(locations=["query_string"],fresh=True)
    def post(self):
        return {
            'message':'success'
        }
        
class GetImagecode(Resource):
    def get(self):
        image, code = validate_picture()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        data = base64.b64encode(buf_str).decode("utf-8")
        code = str(generate_activate_token_forever(code),'utf-8')
        return {'image':data,'code':code}

