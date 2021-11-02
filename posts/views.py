from datetime                           import datetime
from flask                              import request
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful                      import Resource
from flask_jwt_extended                 import get_jwt_identity
from mongoengine                        import Q

from database.models                    import Category, Post


class PostDetailApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user = get_jwt_identity()
            data = request.get_json()
            post = Post(
                title    = data['title'],
                body     = data['body'],
                user     = user,
                category = Category.objects.get(name=data['category'])
            ).save()

            return {'message' : 'SUCCESS', 'post_id' : str(post.id)}, 201

        except KeyError:
            return {'message' : 'KEY_ERROR'}, 400

    @jwt_required()
    def get(self, post_id):
        try:
            user = get_jwt_identity()
            post = Post.objects.get(id=post_id)
            post['read_user'].append(user)
            user_list = list(set(post['read_user']))
            post.update(read_user=user_list)
            post_info = {
                'category'   : post.category.name,
                'title'      : post.title,
                'body'       : post.body,
                'user'       : post.user.email,
                'read_user'  : len(user_list),
                'updated_at' : '{}'.format(post.updated_at)
            }
            
            return post_info, 200

        except Post.DoesNotExist:
            return {'message' : 'POST_DOES_NOT_EXIST'}, 400

    @jwt_required()
    def delete(self, post_id):
        try:
            user = get_jwt_identity()
            Post.objects.get(id=post_id, user=user).delete()

            return {'message' : 'SUCCESS'}, 200

        except Post.DoesNotExist:
            return {'message' : 'POST_DOES_NOT_EXIST'}, 400

    @jwt_required()
    def put(self, post_id):
        try:
            data = request.get_json()
            user = get_jwt_identity()
            post = Post.objects.get(id=post_id, user=user)
            post.update(updated_at=datetime.utcnow, **data)

            return {'message' : 'SUCCESS'}, 200

        except KeyError:
            return {'message' : 'KEY_ERROR'}, 400

        except Post.DoesNotExist:
            return {'message' : 'POST_DOES_NOT_EXIST'}, 400

class PostsApi(Resource):
    def get(self):
        try:
            offset         = int(request.args.get('offset', 0))
            limit          = int(request.args.get('limit', 8))
            category       = request.args.get('category')
            search_word    = request.args.get('search-word', '')
            post_filtering = Q(title__contains=search_word)
            post_filtering |= Q(body__contains=search_word)

            if category:
                post_filtering &= Q(category=category)

            posts  = Post.objects.filter(post_filtering)[offset:offset+limit]

            post = [{
                'category'   : post.category.name,
                'title'      : post.title,
                'body'       : post.body,
                'user'       : post.user.email,
                'read_user'  : len(post.read_user),
                'updated_at' : '{}'.format(post.updated_at)
            } for post in posts]

            return post, 200

        except KeyError:
            return {'message' : 'KEY_ERROR'}, 400