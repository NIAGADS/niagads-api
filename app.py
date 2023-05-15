from flask import Flask
from blueprints.variant import variant_blueprint

app = Flask(__name__)
app.register_blueprint(variant_blueprint)
