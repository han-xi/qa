

from flask_restful import Resource, reqparse
from models.user import User
from models.trash import Trash
from models.question import Question,WrongQuestion,CollectQuestion
from models.classes  import Class,ClassStudent,ClassTeacher
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
import datetime
from flask import jsonify
import bson
import re
parser = reqparse.RequestParser()
parser.add_argument(
    'class_id', help='This field cannot be blank', required=False)
parser.add_argument(
    'user_id', help='This field cannot be blank', required=False)
parser.add_argument(
    'page', required=False)
parser.add_argument(
    'class_name', required=False)
parser.add_argument(
    'type', required=False)
parser.add_argument(
    'content', required=False)
parser.add_argument(
    'date', required=False)
parser.add_argument(
    'current', required=False)
parser.add_argument(
    'search', required=False)
parser.add_argument(
    'search1', required=False)

parser.add_argument(
    'sorter', required=False)
parser.add_argument(
    'limitnum', required=False)
class GetClassResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        current_class = Class.objects(id = bson.ObjectId(data['class_id'])).first()
        current_teacher = ClassTeacher.objects(class_id = data['class_id'],activate=True).all()
        student_num =  ClassStudent.objects(class_id = data['class_id'],activate=True).count()
        teacher_id = []
        if current_teacher:
            for item in current_teacher:
                teacher_id.append({'name':item.teacher_id,'id':item.teacher_id})
        if datetime.datetime.now()>current_class.starttime and datetime.datetime.now()<current_class.endtime:
            status = 1
        elif datetime.datetime.now()<current_class.starttime:
            status = 0
        else:
            status =2
        
        if current_class:
            return {
                'key': '{}'.format(current_class.id),
                'name': '{}'.format(current_class.classname),
                'registertime': '{}'.format(current_class.registertime.strftime("%Y-%m-%d %H:%M:%S")),
                'teacher':'{}'.format(teacher_id),
                'student_num':'{}'.format(student_num),
                'limitnum':'{}'.format(current_class.limitnum),
                'content':'{}'.format(current_class.content),
                'status':'{}'.format(status),
            }
        else:
            return {'message':'未找到'},404
class PostClassResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()  
        userIdentity = get_jwt_identity()
        user =User.objects(username = userIdentity['user']).first()
        if user and user.usertype==2:
            current_teacher = ClassTeacher.objects(class_id= data['class_id'],activate=True).first()
            if current_teacher:
                current_class = Class.objects(id = bson.ObjectId(data['class_id'])).first()
                if current_class:
                    try:
                        current_class.update(content=data['content'])
                        return  {'message': '修改完成'}
                    except:
                        return  {'message': 'Something went wrong'}, 500
            else:
                return {'message':'未授权'},403
        elif user and user.usertype>2:
            current_class = Class.objects(id = bson.ObjectId(data['class_id'])).first()
            if current_class:
                if data['class_name']!=current_class.classname:
                    current_class_name = Class.objects(classname= data['class_name']).first()
                    if current_class_name:
                        return {'message':'该名字已存在'},403
                try:
                    
                    current_class.update(content=data['content'],classname = data['class_name'],limitnum = data['limitnum'])
                    # current_class.update(content=data['content'])
                    return  {'message': '修改完成'}
                except:
                    return  {'message': 'Something went wrong'}, 500
            else:
                return {'message':'未找到'},404 
        else:
            return {'message':'未授权'},403            
               
class GetClassListResource(Resource):
    @jwt_required()
    def post(self):
        current_class=''
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user =User.objects(username = userIdentity['user']).first()
        sorter = data['sorter']
        if data['search']=='':
            SearchClass = Class.objects().all()
            total = len(SearchClass)
        else:               
            regex = re.compile('.*'+data['search']+'.*')
            SearchClass = Class.objects(classname = regex).all()
            total = len(SearchClass)
        if sorter=='ascend':
            current_class = SearchClass.order_by('registertime').paginate(
                page=int(data['current']), per_page=5).items               
        elif sorter=='descend':

            current_class = SearchClass.order_by('-registertime').paginate(
                page=int(data['current']), per_page=5).items                 
        else:            
            current_class = SearchClass.paginate(
            page=int(data['current']), per_page=5).items     
        if user and user.usertype==2: 
            current_teacher = ClassTeacher.objects(teacher_id = userIdentity['user']).all()
            classes_teacher = []
            classes_teacher_apply = []
            for item in current_teacher:
                if item.activate:
                    classes_teacher.append(item.class_id)
                else:
                    classes_teacher_apply.append(item.class_id)
            
            for item in current_class:
                result.append({
            'key': '{}'.format(item.id),
            'name': '{}'.format(item.classname),
            'registertime': '{}'.format(item.registertime.strftime("%Y-%m-%d %H:%M:%S")),
            # 'isstudent':True if str(item.id) in classes_student else False,
            'isteacher':True if str(item.id) in classes_teacher else False,
            # 'isstudentapply':True if str(item.id) in classes_student_apply else False,
            'isteacherapply':True if str(item.id) in classes_teacher_apply else False,
        })
        elif user and user.usertype>2:
           
            for item in current_class:
                result.append({
            'key': '{}'.format(item.id),
            'name': '{}'.format(item.classname),
            'registertime': '{}'.format(item.registertime.strftime("%Y-%m-%d %H:%M:%S")),
            # 'isstudent':True ,
            # 'isteacher':True ,
            # 'isstudentapply':False,
            # 'isteacherapply':False
        })
        else:
            current_student = ClassStudent.objects(student_id = userIdentity['user']).all()
            classes_student = []
            classes_student_apply =[]
            for item in current_student:
                print(item.activate)
                if item.activate:
                    classes_student.append(item.class_id)
                else:
                    classes_student_apply.append(item.class_id)
            if current_class:
                for item in current_class:
                    result.append({
                'key': '{}'.format(item.id),
                # 'key': '{}'.format(bson.ObjectId(item.id).__str__),
                'name': '{}'.format(item.classname),
                'registertime': '{}'.format(item.registertime.strftime("%Y-%m-%d %H:%M:%S")),
                'isstudent':True if str(item.id) in classes_student else False,
                # 'isteacher':False,
                'isstudentapply':True if str(item.id) in classes_student_apply else False,
                # 'isteacherapply':False,
            })
        return{'result':result,'total':total}, 200
class GetStudentResource(Resource):
    @jwt_required()
    def post(self):
        current_class=''
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user =User.objects(username = userIdentity['user']).first()
        if user and user.usertype==2:
            teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],class_id = data['class_id'],activate=True).first()
            if teacher:
                pass
            else:
                return {'message':'未授权'},403
        elif user and user.usertype>2:
            pass
        elif user and user.usertype==1:
            student = ClassStudent.objects(student_id = userIdentity['user'],class_id = data['class_id'],activate=True).first()
            if student:
                pass            
        else:
            return {'message':'未授权'},403
        if user.usertype<3:
            current_class = ClassStudent.objects(class_id = data['class_id'],student_id = data['user_id']).first()
            if current_class:
                pass
            else:
                return {'message':'该班级不存在此学生'},404
        current_user = User.objects(username=data['user_id']).first()
        return   {
            'key': '{}'.format(current_user.username),
            'name': '{}'.format(current_user.username),
            'registertime': '{}'.format(current_user.registertime.strftime("%Y-%m-%d %H:%M:%S")),
            'status':'{}'.format(current_user.islogin),
        }, 200


class GetStudentListResource(Resource):
    @jwt_required()
    def post(self):
        current_class=''
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user =User.objects(username = userIdentity['user']).first()

        if user and user.usertype==2:
            teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],class_id = data['class_id'],activate=True).first()
            if teacher:
                pass
            else:
                return {'message':'没有权限访问，请申请加入班级'}
        elif user and user.usertype>2:
            pass
        else:
            student = ClassStudent.objects(student_id = userIdentity['user'],class_id = data['class_id'],activate=True).first()
            print(student)
            if student:
                pass
            else:
                return {'message':'没有权限访问，请申请加入班级'}                
        # current_class = ClassStudent.objects(class_id = data['class_id'],activate=True).all()
        sorter = data['sorter']
        if data['search']=='':
            if sorter=='ascend':
                SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).order_by('activatetime').all()
            elif sorter=='descend':
                SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).order_by('-activatetime').all()
            else:
                 SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).all()
               
            classids=[]
            for item in SearchClass:
                classids.append(item.student_id)
            SearchStudent = User.objects(username__in = classids)
            total = len(SearchStudent)
        else:        
            if sorter=='ascend':
                SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).order_by('activatetime').all()
            elif sorter=='descend':
                SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).order_by('-activatetime').all()
            else:
                 SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).all()
                    
            regex = re.compile('.*'+data['search']+'.*')
            # SearchClass = ClassStudent.objects(class_id = data['class_id'],activate=True).all()
            classids=[]
            for item in SearchClass:
                classids.append(item.student_id)
            SearchStudent = User.objects(username__in = classids,username = regex)
            total = len(SearchStudent)
        current_class = SearchStudent.paginate(
                page=int(data['current']), per_page=5).items             
        userid=[]
        for item in current_class:
            userid.append(item.username)
        if SearchClass:
            for item in SearchClass:
                if item.student_id in userid:
                    result.append({
                            'key': '{}'.format(item.student_id),
                        'name': '{}'.format(item.student_id),
                        'registertime': '{}'.format(item.activatetime.strftime("%Y-%m-%d %H:%M:%S")),
                        })
                    
        return {'result':result,'total':total}, 200
class AddClassResource(Resource):
    @jwt_required()
    def post(self):

        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user =User.objects(username = userIdentity['user']).first()
        if data['content'] ==None:
            data['content'] ="欢迎欢迎"
        if data['date'] ==None:
            return {'message':'请选择时间'},400
        date = [int(item)for item in data['date'].split(',')]
        starttime = datetime.datetime.utcfromtimestamp(date[0])
        endtime = datetime.datetime.utcfromtimestamp(date[1])
        if user and user.usertype>2:
            newClass = Class(classname = data['class_name'],insertname = userIdentity['user'],content = data['content'],limitnum = data['limitnum'],starttime = starttime,endtime=endtime)
            try:
                newClass.save()
                response_object =  {'message':'Class {} was added'.format(data['class_name'])}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        else:
            response_object = {'message':'未授权'},403 
        return response_object
class DeleteClassResource(Resource):
    @jwt_required()
    def post(self):
        current_class=''
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user =User.objects(username = userIdentity['user']).first()
        if user and user.usertype>2:
            current_class = Class.objects(id = bson.ObjectId(data['class_id'])).first()
            if not current_class:
                response_object = {'message':'资源不存在'}
            else:
                try:
                    current_class.delete()
                    ClassStudent.objects(class_id=data['class_id']).all().delete()
                    ClassTeacher.objects(class_id=data['class_id']).all().delete()
                    response_object = {'message':'资源已删除'}
                except:
                    response_object = {'message': 'Something went wrong'}, 500   
        else:
            response_object = {'message':'未授权'},403 
        return response_object
class AddStudentResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user =User.objects(username = userIdentity['user']).first()
        if not data['user_id']:
            user_id = userIdentity['user']
        else:
            user_id = data['user_id']
        if user and user.usertype>2:
            current_classstudent = ClassStudent.objects(class_id = data['class_id'],student_id = user_id).first()
            if not current_classstudent:
                newClass = ClassStudent(class_id = data['class_id'],student_id = user_id,insertname = userIdentity['user'],activate = True,activatename=userIdentity['user'],activatetime=datetime.datetime.now)
                try:
                    newClass.save()
                    response_object =  {'message':'Class {} was added'.format(data['class_id'])}
                except:
                    response_object = {'message': 'Something went wrong'}, 500
            else:
                if current_classstudent.activate:
                    response_object = {'message': 'is existed'}
                else:
                    try:
                        current_classstudent.update(activate= True,activatename=userIdentity['user'],activatetime=datetime.datetime.now)
                        response_object =  {'message':'审核通过'}
                    except:
                        response_object = {'message': 'Something went wrong'}, 500
        elif user and user.usertype==2:
            current_teacher = ClassTeacher.objects(class_id =data['class_id'],teacher_id = userIdentity['user'],activate=True).first()
            if current_teacher:
                current_classstudent = ClassStudent.objects(class_id = data['class_id'],student_id = user_id).first()
                if not current_classstudent:
                    newClass = ClassStudent(class_id = data['class_id'],student_id = user_id,insertname = userIdentity['user'],activate = True,activatename=userIdentity['user'],activatetime=datetime.datetime.now)
                    try:
                        newClass.save()
                        response_object =  {'message':'Class {} was added'.format(data['class_id'])}
                    except:
                        response_object = {'message': 'Something went wrong'}, 500
                else:
                    if current_classstudent.activate:
                        response_object = {'message': 'is existed'}
                    else:
                        try:
                            current_classstudent.update(activate= True,activatename=userIdentity['user'],activatetime=datetime.datetime.now)
                            response_object =  {'message':'审核通过'}
                        except:
                            response_object = {'message': 'Something went wrong'}, 500
            else:
                response_object = {'message':'未授权'},403 
        else:
            response_object = {'message':'未授权'},403 
        return response_object
class DeleteStudentResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user =User.objects(username = userIdentity['user']).first()
        if not data['user_id']:
            user_id = userIdentity['user']
        else:
            user_id = data['user_id']
        if data['type']:
            operate = data['type']
        else:
            operate = 'notadmit'
        if user :
            if operate =='notadmit':
                if user.usertype>1:
                    if user.usertype==2:
                        current_teacher = ClassTeacher.objects(class_id= data['class_id'],teacher_id = userIdentity['user'],activate = True).first()
                        if current_teacher:
                            pass
                        else:
                            return {'message':'未授权'},403
                    current_classstudent = ClassStudent.objects(class_id = data['class_id'],student_id = user_id,activate=False).first()
                    if current_classstudent:
                        try:
                            newTrash = Trash(class_id =data['class_id'],user_id = user_id,insert_type="ClassStudent" )
                            current_classstudent.delete()
                            newTrash.save()
                            response_object =  {'message':'驳回完成'}
                        except:
                            response_object = {'message': 'Something went wrong'}, 500
                    else:
                        response_object = {'message': '驳回完成'}
                else:
                    return {'message':'未授权'},403
            elif operate =='delete':
                if user.usertype==2:
                    current_teacher = ClassTeacher.objects(class_id= data['class_id'],teacher_id = userIdentity['user'],activate = True).first()
                    if current_teacher:
                        pass
                    else:
                        return {'message':'未授权'},403
                elif user.usertype ==1:
                    current_student = ClassStudent.objects(class_id= data['class_id'],student_id = userIdentity['user'],activate = True).first()
                    if current_student:
                        pass
                    else:
                        return {'message':'未授权'},403                    
                current_classstudent = ClassStudent.objects(class_id = data['class_id'],student_id = user_id,activate=True).first()
                if current_classstudent:
                    try:
                        current_classstudent.delete()
                        response_object =  {'message':'删除完成'}
                    except:
                        response_object = {'message': 'Something went wrong'}, 500
                else:
                    response_object = {'message': '删除完成'} 
            else:
                response_object = {'message': '未授权'},403      
        else:
            response_object = {'message':'未授权'},403
        return response_object     
class GetTeacherResource(Resource):
    @jwt_required()
    def post(self):
        current_class=''
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user =User.objects(username = userIdentity['user']).first()
        if user and user.usertype==2:
            teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],class_id = data['class_id'],activate=True).first()
            if teacher:
                pass
            else:
                return {'message':'未授权'},403
        elif user and user.usertype>2:
            pass
        elif user and user.usertype==1:
            student = ClassStudent.objects(student_id = userIdentity['user'],class_id = data['class_id'],activate=True).first()
            if student:
                pass            
        else:
            return {'message':'未授权'},403
        if user.usertype<3:
            current_class = ClassTeacher.objects(class_id = data['class_id'],teacher_id = data['user_id'],activate=True).first()
            if current_class:
                pass
            else:
                return {'message':'该班级不存在此老师'},404
        current_user = User.objects(username=data['user_id']).first()

        return   {
            'key': '{}'.format(current_user.username),
            'name': '{}'.format(current_user.username),
            'registertime': '{}'.format(current_user.registertime.strftime("%Y-%m-%d %H:%M:%S")),
            'status':'{}'.format(current_user.islogin),
        }, 200

     
class AddTeacherResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user =User.objects(username = userIdentity['user']).first()
        if not data['user_id']:
            user_id = userIdentity['user']
        else:
            user_id = data['user_id']
        if user and user.usertype==3:
            current_classstudent = ClassTeacher.objects(class_id = data['class_id'],teacher_id = user_id).first()
            if not current_classstudent:
                newClass = ClassTeacher(class_id = data['class_id'],teacher_id = user_id,insertname = userIdentity['user'],activate = True,activatename=userIdentity['user'],activatetime=datetime.datetime.now)
                try:
                    newClass.save()
                    response_object =  {'message':'Class {} was added'.format(data['class_id'])}
                except:
                    response_object = {'message': 'Something went wrong'}, 500
            else:
                if current_classstudent.activate:
                    response_object = {'message': 'is existed'}
                else:
                    try:
                        current_classstudent.update(activate= True,activatename=userIdentity['user'],activatetime=datetime.datetime.now)
                        response_object =  {'message':'审核通过'}
                    except:
                        response_object = {'message': 'Something went wrong'}, 500

            
        else:
            response_object = {'message':'未授权'},403 
        return response_object
class DeleteTeacherResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user =User.objects(username = userIdentity['user']).first()
        if not data['user_id']:
            user_id = userIdentity['user']
        else:
            user_id = data['user_id']
        if data['type']:
            operate = data['type']
        else:
            operate = 'notadmit'
        if user and user.usertype>1:
            if operate =='notadmit':
                if user.usertype>2:
                    current_classstudent = ClassTeacher.objects(class_id = data['class_id'],teacher_id = user_id,activate=False).first()
                    if current_classstudent:
                        try:
                            newTrash = Trash(class_id =data['class_id'],user_id = user_id,insert_type="ClassTeacher" )
                            current_classstudent.delete()
                            newTrash.save()
                            response_object =  {'message':'驳回完成'} 
                        except:
                            response_object = {'message': 'Something went wrong'}, 500
                    else:
                        response_object = {'message': '驳回完成'}
                else:
                    response_object = {'message':'未授权'},403
            elif operate =='delete':
                if user.usertype==2:
                    current_teacher = ClassTeacher.objects(class_id = data['class_id'],teacher_id = userIdentity['user'],activate=True).first()
                    if current_teacher:
                        pass
                    else:
                        response_object = {'message':'未授权'},403
                current_classstudent = ClassTeacher.objects(class_id = data['class_id'],teacher_id = user_id,activate=True).first()
                if current_classstudent:
                    try:
                        current_classstudent.delete()
                        response_object =  {'message':'删除完成'}
                    except:
                        response_object = {'message': 'Something went wrong'}, 500
                else:
                    response_object = {'message': '删除完成'} 
            else:
                response_object = {'message': '非法操作'},403      
        else:
            response_object = {'message':'未授权'},403
        return response_object   
class ApplyStudentResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        current_class = Class.objects(id = bson.ObjectId(data['class_id'])).first()
        if current_class:
           class_count= ClassStudent.objects(class_id = data['class_id'],activate =True).count()
           if class_count>current_class['limitnum']:
               return {'message':'人数已满'},403
        current_classstudent = ClassStudent.objects(class_id = data['class_id'],student_id = userIdentity['user']).first()
        if not current_classstudent:
            newClass = ClassStudent(class_id = data['class_id'],student_id = userIdentity['user'],insertname = userIdentity['user'])
            try:
                newClass.save()
                response_object =  {'message':'申请已提交'}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        else:
            if current_classstudent.activate:
                response_object = {'message': 'is existed'}
            else:
                response_object = {'message': '正待审核，请耐心等待'}
        return response_object
class GetApplyStudentListResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user = User.objects(username=userIdentity['user']).first()
        if user and int(user.usertype)==3:
            if data['search'] !='' and data['search1']!='':
                regex = re.compile('.*'+data['search1']+'.*')
                current_class = Class.objects(classname = regex).all()
                class_ids = []
                for item in current_class:
                    class_ids.append(str(item.id))  
                regex = re.compile('.*'+data['search']+'.*')              
                current_apply = ClassStudent.objects(activate=False,student_id=regex,class_id__in = class_ids)
            elif data['search']!='':
                regex = re.compile('.*'+data['search']+'.*')
                current_apply = ClassStudent.objects(activate=False,student_id=regex).all()
            elif data['search1']!='':
                regex = re.compile('.*'+data['search1']+'.*')
                current_class = Class.objects(classname = regex).all()
                class_ids = []
                for item in current_class:
                    class_ids.append(str(item.id))
                current_apply = ClassStudent.objects(activate=False,class_id__in = class_ids)
            else:
                current_apply = ClassStudent.objects(activate=False).all()
            if data['sorter']=='ascend':
                current_apply =current_apply.order_by('updatetime').paginate(
                page=int(data['current']), per_page=5).items  
            elif data['sorter'] =='descend':
                current_apply=current_apply.order_by('-updatetime').paginate(
                page=int(data['current']), per_page=5).items  
            else:
                current_apply=current_apply.paginate(
                page=int(data['current']), per_page=5).items                  
            user_ids=[]
            class_ids = []
            for item in current_apply:
                class_ids.append(bson.ObjectId(item.class_id))
            current_class=   Class.objects(id__in = class_ids)
            class_names = {}
            for item in current_class:
                class_names[str(item.id)] = item.classname
            total = len(class_ids)
            for item in current_apply:
                result.append({
                    'key':'{}'.format(item.id),
                    'username':'{}'.format(item.student_id),
                    'class_id': item.class_id,
                    'class_name':class_names[item.class_id],
                    'updatetime':'{}'.format(item.updatetime.strftime("%Y-%m-%d %H:%M:%S")),
                    'isoperated':False
                })
            return {'result':result,'total':total} 
        elif user and int(user.usertype)==2:
            class_ids =[]
            if data['search'] !='' and data['search1']!='':
                regex = re.compile('.*'+data['search1']+'.*')
                current_teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],activate=True).all()
                class_ids1 = []
                for item in current_teacher:
                    class_ids1.append(item.class_id)
                current_class = Class.objects(classname = regex).all()
                class_ids2 = []
                for item in current_class:
                    class_ids2.append(str(item.id))  
                class_ids =list(set(class_ids1) &set(class_ids2))
                regex = re.compile('.*'+data['search']+'.*')              
                current_apply = ClassStudent.objects(activate=False,student_id=regex,class_id__in =class_ids)
            elif data['search']!='':
                regex = re.compile('.*'+data['search']+'.*')
                current_apply = ClassStudent.objects(activate=False,student_id=regex).all()   
                current_teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],activate=True).all()
                for item in current_teacher:
                    class_ids.append(item.class_id)
                current_apply = ClassStudent.objects(activate=False,student_id=regex,class_id__in =class_ids)                
            elif data['search1']!='':
                regex = re.compile('.*'+data['search1']+'.*')
                current_teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],activate=True).all()
                class_ids1 = []
                for item in current_teacher:
                    class_ids1.append(item.class_id)

                current_class = Class.objects(classname = regex).all()
                class_ids2 = []
                for item in current_class:
                    class_ids2.append(str(item.id))  
                class_ids =list(set(class_ids1) &set(class_ids2))
                current_apply = ClassStudent.objects(activate=False,class_id__in =class_ids)

            else:
                current_apply = ClassStudent.objects(activate=False).all()
                current_teacher = ClassTeacher.objects(teacher_id = userIdentity['user'],activate=True).all()
                for item in current_teacher:
                    class_ids.append(item.class_id)
                current_apply = ClassStudent.objects(activate=False,class_id__in =class_ids)
            if data['sorter']=='ascend':
                current_apply =current_apply.order_by('updatetime').paginate(
                page=int(data['current']), per_page=5).items  
            elif data['sorter'] =='descend':
                current_apply=current_apply.order_by('-updatetime').paginate(
                page=int(data['current']), per_page=5).items  
            else:
                current_apply=current_apply.paginate(
                page=int(data['current']), per_page=5).items                  
            # current_apply = ClassStudent.objects(class_id__in=class_ids,activate=False)
            user_ids=[]
            new_class_ids = []
           
            for item in current_apply:
                new_class_ids.append(bson.ObjectId(item.class_id))
         
            total = len(new_class_ids)
            current_class=  Class.objects(id__in = new_class_ids)
            class_names = {}
            for item in current_class:
                class_names[str(item.id)] = item.classname
            for item in current_apply:
                if item.class_id in class_ids:
                    result.append({
                        'key':'{}'.format(item.id),
                        'username':'{}'.format(item.student_id),
                        'class_id': item.class_id,
                        'class_name':class_names[item.class_id],
                        'updatetime':'{}'.format(item.updatetime.strftime("%Y-%m-%d %H:%M:%S")),
                        'isoperated':False
                    })
            return {'result':result,'total':total} 
        else:
            return {'message':'权限低'}
class ApplyTeacherResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user = User.objects(username=userIdentity['user']).first()
        if user and int(user.usertype)>1:
            current_classteacher = ClassTeacher.objects(class_id = data['class_id'],teacher_id = userIdentity['user']).first()
            if not current_classteacher:
                newClass = ClassTeacher(class_id = data['class_id'],teacher_id = userIdentity['user'],insertname = userIdentity['user'])
                try:
                    newClass.save()
                    response_object =  {'message':'申请已提交'}
                except:
                    response_object = {'message': 'Something went wrong'}, 500
            else:
                if current_classteacher.activate:
                    response_object = {'message': 'is existed'}
                else:
                    response_object = {'message': '正待审核，请耐心等待'}
            return response_object
        else:
            return {'message':'未授权'},403

class GetApplyTeacherListResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user = User.objects(username=userIdentity['user']).first()
        if user and int(user.usertype)>2:
            if data['search'] !='' and data['search1']!='':
                regex = re.compile('.*'+data['search1']+'.*')
                current_class = Class.objects(classname = regex).all()
                class_ids = []
                for item in current_class:
                    class_ids.append(str(item.id))  
                regex = re.compile('.*'+data['search']+'.*')              
                current_apply = ClassTeacher.objects(activate=False,teacher_id=regex,class_id__in = class_ids)
            elif data['search']!='':
                regex = re.compile('.*'+data['search']+'.*')
                current_apply = ClassTeacher.objects(activate=False,teacher_id=regex).all()
            elif data['search1']!='':
                regex = re.compile('.*'+data['search1']+'.*')
                current_class = Class.objects(classname = regex).all()
                class_ids = []
                for item in current_class:
                    class_ids.append(str(item.id))
                current_apply = ClassTeacher.objects(activate=False,class_id__in = class_ids)
            else:
                current_apply = ClassTeacher.objects(activate=False).all()
            if data['sorter']=='ascend':
                current_apply =current_apply.order_by('updatetime').paginate(
                page=int(data['current']), per_page=5).items  
            elif data['sorter'] =='descend':
                current_apply=current_apply.order_by('-updatetime').paginate(
                page=int(data['current']), per_page=5).items        
            else:
                current_apply=current_apply.order_by('-updatetime').paginate(
                page=int(data['current']), per_page=5).items                 
            user_ids=[]
            class_ids = []
            for item in current_apply:
                class_ids.append(bson.ObjectId(item.class_id))
            total = len(class_ids)
            current_class=   Class.objects(id__in = class_ids)
            class_names = {}
            for item in current_class:
                class_names[str(item.id)] = item.classname
            
            for item in current_apply:
                result.append({
                    'key':'{}'.format(item.id),
                    'username':'{}'.format(item.teacher_id),
                    'class_id': item.class_id,
                    'class_name':class_names[item.class_id],
                    'updatetime':'{}'.format(item.updatetime.strftime("%Y-%m-%d %H:%M:%S")),
                    'isoperated':False
                })
            return {'result':result,'total':total} 
        else:
            return {'message':'权限低'}
        
        
        
        
class GetMessageInfoResource(Resource):
    @jwt_required()
    def get(self):
        result=[]
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user = User.objects(username=userIdentity['user']).first()
        if user and int(user.usertype)==1:
            current_student = ClassStudent.objects(student_id =userIdentity['user'],activate = True,ispushmsg=False).all()
            class_ids =[]
            for item in current_student:
                class_ids.append(bson.ObjectId(item.class_id))
            current_trash = Trash.objects(user_id=userIdentity['user'],ispushmsg=False).all()
            for item in current_trash:
                class_ids.append(bson.ObjectId(item.class_id))
            
            current_class = Class.objects(id__in=class_ids)
            class_names = {}
            for item in current_class:
                class_names[str(item.id)]=item.classname
            for item in current_student:
                result.append({'message':'申请加入{0}已通过'.format(class_names[item.class_id]),'time':'{}'.format(item.activatetime.strftime("%Y-%m-%d %H:%M:%S"))})
            for item in current_trash:
                result.append({'message':'申请加入{0}被拒绝'.format(class_names[item.class_id]),'time':'{}'.format(item.inserttime.strftime("%Y-%m-%d %H:%M:%S"))})      
        elif   user and int(user.usertype)==2:  
            current_student = ClassStudent.objects(student_id =userIdentity['user'],activate = True,ispushmsg=False).all()
            class_ids =[]
            for item in current_student:
                class_ids.append(bson.ObjectId(item.class_id))
            current_trash = Trash.objects(user_id=userIdentity['user'],ispushmsg=False).all()
            for item in current_trash:
                class_ids.append(bson.ObjectId(item.class_id))

            current_teacher = ClassTeacher.objects(teacher_id =userIdentity['user'],activate = True,ispushmsg=False).all()
            for item in current_teacher:
                class_ids.append(bson.ObjectId(item.class_id))
           
            current_class = Class.objects(id__in=class_ids)
            class_names = {}
            for item in current_class:
                class_names[str(item.id)]=item.classname
            for item in current_student:
                result.append({'message':'申请加入{0}已通过'.format(class_names[item.class_id]),'time':'{}'.format(item.activatetime.strftime("%Y-%m-%d %H:%M:%S"))})
            for item in current_trash:
                if item.insert_type=="ClassStudent":
                    result.append({'message':'申请加入{0}被拒绝'.format(class_names[item.class_id]),'time':'{}'.format(item.inserttime.strftime("%Y-%m-%d %H:%M:%S"))})    
                else:
                    result.append({'message':'申请在{0}任课被拒绝'.format(class_names[item.class_id]),'time':'{}'.format(item.inserttime.strftime("%Y-%m-%d %H:%M:%S"))})                         
            for item in current_teacher:
                result.append({'message':'申请在{0}任课已通过'.format(class_names[item.class_id]),'time':'{}'.format(item.activatetime.strftime("%Y-%m-%d %H:%M:%S"))})    
        elif   user and int(user.usertype)==3:
            current_student = ClassStudent.objects(activate = False).all()
            current_teacher = ClassTeacher.objects(activate = False).all()
            class_ids =[]
            for item in current_student:
                class_ids.append(bson.ObjectId(item.class_id))
            for item in current_teacher:
                class_ids.append(bson.ObjectId(item.class_id))
            current_class = Class.objects(id__in=class_ids)
            class_names = {}
            for item in current_class:
                class_names[str(item.id)]=item.classname  
            for item in  current_student:
                result.append({'message':'用户:{0}想要申请加入{1}'.format(item.student_id,class_names[item.class_id]),'time':'{}'.format(item.updatetime.strftime("%Y-%m-%d %H:%M:%S"))})
            for item in current_teacher:
                result.append({'message':'用户：{0}想要加入申请在{1}任职'.format(item.tearch_id,class_names[item.class_id]),'time':'{}'.format(item.updatetime.strftime("%Y-%m-%d %H:%M:%S"))})
                                         
        return {'result':result}   
         
class GetMesageCountResource(Resource):
    @jwt_required()
    def get(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()  
        user = User.objects(username=userIdentity['user']).first()
        if user and int(user.usertype)==1:
            count1 = ClassStudent.objects(student_id =userIdentity['user'],activate = True,ispushmsg=False).count()
            count2 = Trash.objects(user_id=userIdentity['user'],ispushmsg=False).count()
            count= count1+count2
            return {'count':count}
        elif user and int(user.usertype)==2:
            count1 = ClassStudent.objects(student_id =userIdentity['user'],activate = True,ispushmsg=False).count()
            count2 = ClassTeacher.objects(teacher_id =userIdentity['user'],activate = True,ispushmsg=False).count()
            count3 = Trash.objects(user_id=userIdentity['user'],ispushmsg=False).count()
            count = count1+count2+count3
            return {'count':count}
        elif user and int(user.usertype)==3:
            count1 = ClassStudent.objects(activate = False).count()
            count2 = ClassTeacher.objects(activate = False).count()
            count = count1+count2
            return {'count':count}

