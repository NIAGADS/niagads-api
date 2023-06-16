from flask import Flask

# local imports
from shared_resources.db import genomicsdb
from shared_resources import niagads_api as api
from config import set_app_config
import logging

def configure_logging(app: Flask):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    if app.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


app = Flask(__name__)
configure_logging(app)
app.config.update(set_app_config())
api.init_app(app)
genomicsdb.init_app(app)


if __name__ == "__main__":
    app.run()
    