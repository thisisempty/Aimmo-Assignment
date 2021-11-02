from users.views import SignInApi, SignUpApi

def initialize_routes(api):
    api.add_resource(SignUpApi, '/users/signup')
    api.add_resource(SignInApi, '/users/signin')