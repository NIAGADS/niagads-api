from os import path
from dotenv import dotenv_values


def get_version():
    basedir = path.abspath(path.dirname(__file__))
    version = dict(dotenv_values(path.join(basedir, ".env")))['API_VERSION']
    return version

    
def set_app_config(initCacheDB=False):
    ''' retrieve app configuration from `.env` files containing 
        key/value config values such as db connection info'''
        
    basedir = path.abspath(path.dirname(__file__))
    
    #. env
    app_config = dict(dotenv_values(path.join(basedir, ".env")))
    app_config = { k : bool(v) if v in ["True", "False"] else v  for k, v in app_config.items()}
    
    # application root
    # app_config['APPLICATION_ROOT'] = '/' + app_config['API_VERSION'] + '/'
    # del app_config['API_VERSION']
    
    # don't want the templated database URI in the config
    # -> process separately
    del app_config['SQLALCHEMY_DATABASE_URI']
    connection_str = dict(dotenv_values(path.join(basedir, ".env")))['SQLALCHEMY_DATABASE_URI']
    db_config = {           
            'filer': "sqlite:///niagads_api_cache.db",
            'cache': "sqlite:///niagads_api_cache.db",
    }
    
    if not initCacheDB:
        # only add GenomicsDB if not updating the cache
        # head off any chance of dropping anything from GenomicsDB database
        del app_config['FILER_METADATA_TEMPLATE_FILE']
        db_config.update({
                'GRCh38' : connection_str.format('genomicsdb'),
                'GRCh37' : connection_str.format('genomicsdb37'),
        })
        

    app_config.update({'SQLALCHEMY_BINDS': db_config})    
    return app_config