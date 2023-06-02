from os import path
from dotenv import dotenv_values

def get_sql_binds():
    ''' retrieve sql binds from `.env` files '''
    basedir = path.abspath(path.dirname(__file__))
    connection_str = dict(dotenv_values(path.join(basedir, "genomicsdb.env")))['SQLALCHEMY_DATABASE_URI']
    return {
            'GRCh38' : connection_str.format('genomicsdb'),
            'GRCh37' : connection_str.format('genomicsdb37'),
            '__all__': connection_str
            }


def set_app_config():
    ''' retrieve app configuration from `.env` files containing 
        key/value config values such as db connection info'''
        
    basedir = path.abspath(path.dirname(__file__))

    #. env
    app_config = dict(dotenv_values(path.join(basedir, ".env")))
 
    # genomicsdb.env
    genomicsdb_config = {'SQLALCHEMY_BINDS' : get_sql_binds()}

    app_config.update(genomicsdb_config)    
    return app_config