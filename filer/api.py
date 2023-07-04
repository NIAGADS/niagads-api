from flask_restx import Namespace, Resource, fields

from shared_resources.schemas.about import api_root_information
from shared_resources.fields.genome_build import GenomeBuild
from shared_resources.parsers import arg_parsers as parsers
from shared_resources import constants 

# child APIs
from filer.track.api import api as track_api

CHILD_APIS = [track_api]

description = "API Calls for accessing FILER, the NIAGADS functional genomics repository"
api = Namespace('filer', description=description)

model = api.model('API Info', api_root_information)
parser = parsers.genome_build

@api.route('/')
class Filer(Resource):
    @api.marshal_with(model, envelope='filer')
    def get(self):
        args = parsers.parse_args()
        return {"endpoint": "/filer",
                "resource_url": constants.URLS.filer,
                "organization": "NIAGADS", 
                "organization_url": constants.URLS.niagads,
                "description": description
                }
