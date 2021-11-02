import json

from flask                              import request
from time                               import strftime, strptime
from flask                              import request
from flask_restful                      import Resource
from database.models                    import Comment, Reply, Post, User
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended                 import get_jwt_identity

class CommentApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user = get_jwt_identity()
            data = request.get_json()
            
            body = data['body']
            
            comment = Comment(
                body    = body,
                user    = user,
                post    = Post.objects.get(id=data['post'])
            ).save()
            
            return {'message' : 'SUCCESS', 'comment_id' : str(comment.id)}, 201

        except KeyError:
            return {'message' : 'KEY-ERROR'}, 400
        
        except Comment.DoesNotExist:
            return {'message' : 'POST_DOES_NOT_EXIST'}, 400
        
    @jwt_required()
    def get(self, comment_id):
        try:
            user = get_jwt_identity()
            comments = Comment.objects.filter(id=comment_id, user=user)
            offset = int(request.args.get('offset',0))
            limit  = int(request.args.get('limit',5))
            
            comment_list = [{
                'post' : comment.post.title,
                'body' : comment.body,
                'user' : comment.user.email,
                'updated_at' : '{}'.format(comment.updated_at)
            }for comment in comments[offset:offset+limit]]
        
            return comment_list, 200
    
        except KeyError:
            return {'message' : 'KEY_ERROR'}, 400

    
    @jwt_required()
    def delete(self, comment_id):
        try:
            user = get_jwt_identity()
            Comment.objects.get(id = comment_id, user=user).delete()
            
            return {'message' : 'SUCCESS'}, 200
        
        except Comment.DoesNotExist:
            return {'message' : 'COMMENT_DOES_NOT_EXIST'}, 400

        except User.DoesNotExist:
            return {'message' : 'USER_DOES_NOT_EXIST'}, 400
        

    
class ReplyApi(Resource):
    @jwt_required() 
    def post(self):  
        try:
            user = get_jwt_identity()
            data = request.get_json() 
            
            reply=Reply(
                user = user,
                comment = Comment.objects.get(id=data['comment']),
                body = data['body']
            ).save()
            
            return {'message' : 'SUCCESS', 'reply_id' : str(reply.id)}, 201

        except KeyError:
            return {'message' : 'KEY_ERROR'}, 400

        except Reply.DoesNotExist:
            return {'message' : 'REPLY_DOES_NOT_EXIST'}, 400
        
        except Comment.DoesNotExist:
            return {'message' : 'COMMENT_DOES_NOT_EXIST'}, 400
            
    def get(self, comment_id):
        try:
            replys = Reply.objects.filter(comment=comment_id)
            offset = int(request.args.get('offset',0))
            limit  = int(request.args.get('limit',5)) 
            
            reply_list = [{
                'user' : reply.user.email,
                'comment' : reply.comment.body,
                'body' : reply.body,
                'updated_at' : '{}'.format(reply.updated_at)
            }for reply in replys[offset:offset+limit]]
        
            return reply_list, 200
    
        except KeyError:
            return {'message' : 'KEY_ERROR'}, 400
        
