from users.views import SignInApi, SignUpApi
from posts.views import PostDetailApi, PostsApi

def initialize_routes(api):
    api.add_resource(SignUpApi, '/users/signup')
    api.add_resource(SignInApi, '/users/signin')
    api.add_resource(PostDetailApi, '/post', '/post/<post_id>')
    api.add_resource(PostsApi, '/posts')