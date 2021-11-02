import datetime

from flask_bcrypt import generate_password_hash, check_password_hash

from run          import db

class User(db.Document):
    email      = db.StringField(required=True, unique=True)
    password   = db.StringField(required=True, min_length=8)
    nickname   = db.StringField(required=True, unique=True)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Category(db.Document):
    name       = db.StringField(required=True, unique=True)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

class Post(db.Document):
    category   = db.ReferenceField(Category, required=True)
    title      = db.StringField(required=True)
    body       = db.StringField(required=True)
    user       = db.ReferenceField(User, required=True)
    read_user  = db.ListField()
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

class Comment(db.Document):
    post       = db.ReferenceField(Post, required=True)
    body       = db.StringField(required=True)
    user       = db.ReferenceField(User, required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

class Reply(db.Document):
    user       = db.ReferenceField(User, required=True)
    comment    = db.ReferenceField(Comment, required=True)
    body       = db.StringField(required=True)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)
