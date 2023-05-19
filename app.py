from flask import Flask
from flask_restx import Api, Resource
from os import path
from dotenv import dotenv_values

# import NIAGADS apis
from db import genomicsdb
from apis import api

def set_app_config():
    ''' retrieve app configuration from `.env` files containing 
        key/value config values such as db connection info'''
        
    basedir = path.join(path.abspath(path.dirname(__file__)), "configs")

    #. env
    app_config = dict(dotenv_values(path.join(basedir, ".env")))
 
    # genomicsdb.env
    genomicsdb_config = dict(dotenv_values(path.join(basedir, "genomicsdb.env")))
    app_config.update(genomicsdb_config)
    
    return app_config

app = Flask(__name__)
app.config.update(set_app_config())
api.init_app(app)
genomicsdb.init_app(app)

if __name__ == "__main__":
    app.run()