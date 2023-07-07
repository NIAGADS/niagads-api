import logging
from os import _exit
from flask import Flask, send_file

# local imports
from shared_resources.db import db
from shared_resources.db_utils import create_tables
from middleware import PrefixMiddleware
from api import api
from config import set_app_config, get_version

def configure_logging(app: Flask):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

    return logging.getLogger(__name__)


def create_app(initCacheDB): 
    app = Flask(__name__)
    logger = configure_logging(app)
    app.config.update(set_app_config(initCacheDB != None))
    prefix = '/' + str(get_version())
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=prefix)
    if not initCacheDB:
        api.init_app(app)
    db.init_app(app)   
    
    if initCacheDB:
        logger.info("'initCacheDB' parameter passed, initializing cache database: " + initCacheDB)
        create_tables(db, app, initCacheDB.lower())
        logger.info("DONE initializing cache DB: " + initCacheDB + " / please restart with FLASK_APP=app:create_app(None)")
        _exit(0)

    return app


    

# custom swagger-ui? 
# @app.route('/swaggerui/swagger-ui.css')
# def custom_css_theme():
#       return send_file(
#          path.join(app.root_path, 'ui/custom_swagger.css') 
#       )


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--initCacheDB', choices=['all', 'cache', 'FILER'],
            help="initialize or reinitialize DB cache: FILER - FILER metadata, cache - query cache, all - both")
    args = parser.parse_args()

    app = create_app(args.initDB)
    
    app.run()
    
    