from users.views import SignInApi, SignUpApi
from comments.views import CommentApi, ReplyApi
from posts.views import PostDetailApi, PostsApi

def initialize_routes(api):
    api.add_resource(SignUpApi, '/users/signup')
    api.add_resource(SignInApi, '/users/signin')
    
    api.add_resource(CommentApi, '/comment', '/comment/<comment_id>')
    api.add_resource(ReplyApi, '/reply', '/reply/<comment_id>', '/reply/<reply_id>')

    api.add_resource(PostDetailApi, '/post', '/post/<post_id>')
    api.add_resource(PostsApi, '/posts')

