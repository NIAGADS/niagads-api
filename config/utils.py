from os import path
from dotenv import dotenv_values

def set_app_config():
    ''' retrieve app configuration from `.env` files containing 
        key/value config values such as db connection info'''
        
    basedir = path.abspath(path.dirname(__file__))

    #. env
    app_config = dict(dotenv_values(path.join(basedir, ".env")))
 
    # genomicsdb.env
    # genomicsdb_config = dict(dotenv_values(path.join(basedir, "genomicsdb.env")))

    connection_str = dict(dotenv_values(path.join(basedir, "genomicsdb.env")))['SQLALCHEMY_DATABASE_URI']
    genomicsdb_config = {
        'SQLALCHEMY_BINDS' : {
                'GRCh38' : connection_str.format('genomicsdb'),
                'GRCh37' : connection_str.format('genomicsdb37')
        }
    }

    app_config.update(genomicsdb_config)    
    return app_config