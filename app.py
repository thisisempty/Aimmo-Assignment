from flask import Flask
import config

def get_app_with_config(test_config=None):
    app = Flask(__name__)
    
    if test_config == None:
        app.config.from_object(config.Runconfig)
    else:
        app.config.from_object(config.TestConfig)
    
    return app