import os

JWT_SECRET_KEY = os.environ['AIMMO_SECRET']

class Runconfig:
    MONGO_HOST    = '127.0.0.1'
    MONGO_PORT    = 27107
    MONGO_DB_NAME = 'aimmo'
    MONGO_URI     = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"

class TestConfig:
    MONGO_HOST     = '127.0.0.1'
    MONGO_PORT     = 27107
    MONGO_DB_NAME  = 'testdb'
    MONGO_URI      = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}'
    TESTING        = True
    JWT_SECRET_KEY = "test-secret-key"