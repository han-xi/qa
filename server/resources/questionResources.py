
from flask_restful import Resource, reqparse
from models.user import User
from models.question import Question, WrongQuestion, CollectQuestion
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from datetime import datetime
from flask import jsonify
import bson
parser = reqparse.RequestParser()
parser.add_argument(
    'problem_id', help='This field cannot be blank', required=False)
parser.add_argument(
    'user_id', help='This field cannot be blank', required=False)
parser.add_argument(
    'page', required=False)
parser.add_argument(
    'size', required=False)
parser.add_argument(
    'wrong_answer', required=False)
parser.add_argument(
    'problem', required=False)
parser.add_argument(
    'answer', required=False)
parser.add_argument(
    'options', required=False)
parser.add_argument(
    'tags', required=False)
parser.add_argument(
    'class_id', required=False)


class GetQuestionResource(Resource):
    # @jwt_required
    def post(self):
        data = parser.parse_args()
        # userIdentity = get_jwt_identity()
        current_problem = Question.objects(
            _id=bson.ObjectId(data['problem_id'])).first()
        return {
            'problem_id': '{}'.format(current_problem.id),
            'problem': '{}'.format(current_problem.problem),
            'options': '{}'.format(current_problem.options),
            'answer': '{}'.format(current_problem.answer),
        }, 200


class GetQuestionListResource(Resource):
    @jwt_required(optional=True)
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        current_problem = Question.objects.paginate(
            page=int(data['page']), per_page=10).items
        # TODO exist collect
        current_collect_ids=[]
        if userIdentity:
            problem_ids = []
            for item in current_problem:
                problem_ids.append(str(item.id))
            problem_ids.sort()
            print(problem_ids)
            current_collect = CollectQuestion.objects(problem_id__in = problem_ids,user_id = userIdentity['user'])
            print(current_collect)
            current_collect_ids = [item.problem_id for item in current_collect]
        for ind, item in enumerate(current_problem):
            result.append({
                'Index': (int(data['page'])-1)*10+ind+1,
                'Problem_id': '{}'.format(item.id),
                'Title': '{}'.format(item.problem),
                'Options': '{}'.format(item.options),
                'Answer': '{}'.format(item.answer),
                'IsCollected':True if str(item.id) in current_collect_ids else False  
            })

        return {'result': result}, 200


class AddQuestionResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        user = User.objects(username=userIdentity['user']).first()
        if data['tags']=='':
            data['tags'] =[]
        data['tags'] = [item for item in data['tags'].split(',')]
        if data['class_id'] =='':
            data['class_id'] =[]
        data['class_id'] = [item for item in data['class_id'].split(',')]
        if data['options'] =='':
            return {'message':'输入选项'},400
        data['options'] = [item for item in data['options'].split(',')]
        if user and user.usertype > 2:
            newQuestion = Question(
                problem=data['problem'], options=data['options'], answer=int(data['answer']), tag=data['tags'],class_id=data['class_id'], insertname=userIdentity['user'])
            try:
                newQuestion.save()
                response_object = {
                    'message': 'Question {} was added'.format(data['problem'])}
            except Exception as e:
                print(e)
                
                response_object = {'message': 'Something went wrong'}, 500
        else:
            response_object = {'message': '未授权'},403
        return response_object

class GetWrongQuestionResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        isremain = False
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        current_wrong = WrongQuestion.objects(user_id=userIdentity['user'],problem_id = data['problem_id']).first()
        if current_wrong:
            currrent_question = Question.objects(id = bson.ObjectId(data['problem_id'])).first()
            current_collect = CollectQuestion.objects(problem_id = data['problem_id'],user_id = userIdentity['user'])
            return {
                "Title":'{}'.format(currrent_question.problem),
                "Options":'{}'.format(currrent_question.options),
                "Answer":'{}'.format(currrent_question.answer),
                "Wrong":'{}'.format(current_wrong.wrong_answer),
                "IsCollected":True if current_collect else False
            }
        else:
            return {'message':'未授权'},403
class GetWrongQuestionListResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        isremain = False
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        if not data['size']:
            size = 5
        else:
            size = int(data['size'])
        current_problem_id = WrongQuestion.objects(
            user_id=userIdentity['user']).paginate(page=int(data['page']), per_page=size).items

        if current_problem_id:
            problems_id = []
            for item in current_problem_id:
                problems_id.append(item.problem_id)
            problems_id.sort()
            problems_id = [bson.ObjectId(item) for item in problems_id]
            problem = Question.objects(id__in=problems_id).all()
            for ind,(item1, item2) in enumerate(zip(current_problem_id, problem)):
                result.append({
                    # 'id':(int(data['page'])-1)*5+ind+1,
                    'problem_id': '{}'.format(item1.problem_id),
                    'title': '{}'.format(item2.problem),
                    'updatetime':'{}'.format(item1.updatetime.strftime("%Y-%m-%d %H:%M:%S")),
                    'num':'{}'.format(item1.num)
                    # 'wrong_answer': '{}'.format(item1.wrong_answer)
                })
            isremain = len(current_problem_id) == 5
        return {'result': result, 'isremain': isremain}, 200
class GetWrongQuestionListResourceForHome(Resource):
    @jwt_required()
    def post(self):
        result = []
        isremain = False
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        current_problem_id = WrongQuestion.objects(
            user_id=userIdentity['user']).paginate(page=int(data['page']), per_page=10).items
        if current_problem_id:
            problems_id = []
            for item in current_problem_id:
                problems_id.append(item.problem_id)
            problems_id.sort()
            problem_colllect = problems_id
            problems_id = [bson.ObjectId(item) for item in problems_id]
            current_collect = CollectQuestion.objects(problem_id__in = problem_colllect,user_id = userIdentity['user'])
        
            current_collect_ids = [item.problem_id for item in current_collect]            
            problem = Question.objects(id__in=problems_id).all()
            for ind,(item1, item2) in enumerate(zip(current_problem_id, problem)):
                result.append({
                    'Index': (int(data['page'])-1)*10+ind+1,
                    'Problem_id': '{}'.format(item1.problem_id),
                    'Title': '{}'.format(item2.problem),
                    'Options': '{}'.format(item2.options),
                    'wrong_answer': '{}'.format(item1.wrong_answer),
                    'Answer': '{}'.format(item2.answer),
                    'IsCollected': True if item1.problem_id in current_collect_ids else False
                })
            isremain = len(current_problem_id) == 10
        return {'result': result}, 200


class GetWrongQuestionListResourceByUserid(Resource):
    @jwt_required()
    def post(self):
        result = []
        isremain = False
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        current_user = User.objects(username=userIdentity['user']).first()
        if current_user and current_user.usertype > 1:
            # 根据学生id查询错题
            current_problem_id = WrongQuestion.objects(
                user_id=data['user_id']).paginate(page=data['page'], per_page=10).items
            if current_problem_id:
                problems_id = []
                for item in current_problem_id:
                    problems_id.append(item.problem_id)
                problems_id.sort()
                problems_id = [bson.ObjectId(item) for item in problems_id]
                # 查询问题
                problem = Question.objects(id__in=problems_id).all()
                for item1, item2 in zip(current_problem_id, problem):
                    result.append({
                        'problem_id': '{}'.format(item1.problem_id),
                        'problem': '{}'.format(item2.problem),
                        'wrong_answer': '{}'.format(item1.wrong_answer)
                    })
                isremain = len(current_problem_id) == 10
            return {'result': result, 'isremain': isremain}, 200
        else:
            return {'message': '无权查看'}, 401


class AddWrongQuestionResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        Wrong = WrongQuestion.objects(
            user_id=userIdentity['user'], problem_id=data['problem_id']).first()
        if not Wrong:
            newWrongQuestion = WrongQuestion(
                user_id=userIdentity['user'], problem_id=data['problem_id'], wrong_answer=data['wrong_answer'])
            try:
                newWrongQuestion.save()
                response_object = {
                    'message': 'Problem {} was added'.format(data['problem_id'])}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        else:
            try:
                Wrong.update(num=Wrong.num+1,
                             wrong_answer=data['wrong_answer'])
                response_object = {
                    'message': 'Problem {} was added'.format(data['problem_id'])}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        return jsonify(response_object)


class DeleteWrongQuestionResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        todelete = WrongQuestion.objects(
            user_id=userIdentity['user'], problem_id=data['problem_id']).first()
        if not todelete:
            response_object = {'message': '资源不存在'}
        else:
            try:
                todelete.delete()
                response_object = {'message': '资源已删除'}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        return jsonify(response_object)


class GetCollectQuestionResource(Resource):
    @jwt_required()
    def post(self):
        result = []
        isremain = False
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        current_problem_id = CollectQuestion.objects(
            user_id=userIdentity['user']).paginate(page=data['page'], per_page=10).items
        if current_problem_id:
            problems_id = []
            for item in current_problem_id:
                problems_id.append(item.problem_id)
            problems_id.sort()
            problems_id = [bson.ObjectId(item) for item in problems_id]
            problem = Question.objects(id__in=problems_id).all()
            for item1, item2 in zip(current_problem_id, problem):
                result.append({
                    'problem_id': '{}'.format(item1.problem_id),
                    'problem': '{}'.format(item2.problem),
                    'wrong_answer': '{}'.format(item1.wrong_answer)
                })
            isremain = len(current_problem_id) == 10
        return {'result': result, 'isremain': isremain}, 200


class AddCollectQuestionResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        collect = CollectQuestion.objects(
            user_id=userIdentity['user'], problem_id=data['problem_id']).first()
        if not collect:
            newCollectQuestion = CollectQuestion(
                user_id=userIdentity['user'], problem_id=data['problem_id'])
            try:
                newCollectQuestion.save()
                response_object = {
                    'message': 'Problem {} was added'.format(data['problem_id'])}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        else:
            response_object = {
                'message': 'Problem {} was added'.format(data['problem_id'])}
        return jsonify(response_object)


class DeleteCollectQuestionResource(Resource):
    @jwt_required()
    def post(self):
        data = parser.parse_args()
        userIdentity = get_jwt_identity()
        todelete = CollectQuestion.objects(
            user_id=userIdentity['user'], problem_id=data['problem_id']).first()
        if not todelete:
            response_object = {'message': '资源不存在'}
        else:
            try:
                todelete.delete()
                response_object = {'message': '资源已删除'}
            except:
                response_object = {'message': 'Something went wrong'}, 500
        return jsonify(response_object)
# class CheckCollectQuestionResource(Resource):
#     @jwt_required
#     def post(self):
#         data = parser.parse_args()
#         userIdentity = get_jwt_identity()
#         todelete = CollectQuestion.objects(
#             user_id=userIdentity, problem_id=data['problem_id']).first()           