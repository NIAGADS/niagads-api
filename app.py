from flask import Flask

# local imports
from db import genomicsdb
from base import niagads_api as api
from config import set_app_config

app = Flask(__name__)
app.config.update(set_app_config())
api.init_app(app)
genomicsdb.init_app(app)

if __name__ == "__main__":
    app.run()
    