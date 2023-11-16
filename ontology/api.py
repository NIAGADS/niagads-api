from flask_restx import Namespace, Resource, fields

from shared_resources.schemas.about import api_root_information
from shared_resources.parsers import arg_parsers as parsers
from shared_resources.constants import URLS

# child APIs
# from ontology.validator.api import api as validator_api
from ontology.term.api import api as term_api

CHILD_APIS = [term_api]

description = "API Calls for discovering and validating ontology terms"
api = Namespace('ontology', description=description)

model = api.model('API Info', api_root_information)
@api.route('/')
class Ontology(Resource):
    @api.marshal_with(model)
    def get(self):
        # args = parsers.parse_args()
        return {"endpoint": "/ontology",
                "organization": "NIAGADS", 
                "organization_url": URLS.niagads,
                "description": description
                }
