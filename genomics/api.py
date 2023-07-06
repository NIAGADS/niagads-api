from flask_restx import Namespace, Resource
from marshmallow import ValidationError

from shared_resources.schemas.about import api_root_information
from shared_resources.parsers import arg_parsers as parsers
from shared_resources import constants, utils

# child APIs
from genomics.gene.api import api as gene_api
from genomics.collection.api import api as collection_api
from genomics.track.api import api as track_api

CHILD_APIS = [collection_api, track_api, gene_api]


api = Namespace('genomics', description="API Calls for accessing the NIAGADS Alzheimer's Genomics Database")

schema = api.model('API Info', api_root_information)
parser = parsers.genome_build

@api.route('/')
@api.expect(parser)
class Genomics(Resource):
    @api.marshal_with(schema, envelope='genomics')

    def get(self):
        args = parsers.genome_build.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])
            resourceEndpoint = "genomics" if genomeBuild == 'GRCh38' else "genomics37"
            apiEndpoint = "/genomics" if genomeBuild == 'GRCh38' else "/genomics/?assembly=GRCh37"
            return {"endpoint": apiEndpoint,
                    "resource_url": constants.URLS.niagads + resourceEndpoint,
                    "organization": "NIAGADS", 
                    "organization_url": constants.URLS.niagads,
                    "description": "API Calls for accessing the NIAGADS Alzheimer's Genomics Database (" + genomeBuild + ")"}
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")
