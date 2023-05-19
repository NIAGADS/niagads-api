from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from blueprints import genomics_bp

app = Flask(__name__)
app.register_blueprint(genomics_bp)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='NIAGADS API',
        version='1.0',
        plugins=[MarshmallowPlugin()],
        openapi_version='3.0.2'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)
# docs.register(get_pets, blueprint="genomics")

if __name__ == "__main__":
    app.run()