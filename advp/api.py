from flask_restx import Namespace, Resource, fields

from shared_resources.schemas.about import api_root_information
from shared_resources.fields.genome_build import GenomeBuild
from shared_resources.parsers import arg_parsers as parsers
from shared_resources import constants 

# child APIs
from advp.variant.api import api as variant_api

CHILD_APIS = [variant_api]

description = "API Calls for accessing the Alzheimer's disease Variant Portal (ADVP)"
api = Namespace('advp', description=description)

model = api.model('API Info', api_root_information)
parser = parsers.genome_build
@api.route('/')
class ADVP(Resource):
    @api.marshal_with(model)
    def get(self):
        # args = parsers.parse_args()
        return {"endpoint": "/advp",
                "resource_url": constants.URLS.advp,
                "organization": "NIAGADS", 
                "organization_url": constants.URLS.niagads,
                "description": description
                }
