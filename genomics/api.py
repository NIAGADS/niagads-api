from flask_restx import Namespace, Resource, fields

from shared_resources.schemas.about import api_root_information
from shared_resources.fields.genome_build import GenomeBuild
from shared_resources.parsers import parsers

# child APIs
from genomics.gene.api import api as gene_api
from genomics.dataset.api import api as dataset_api
from genomics.track.api import api as track_api

CHILD_APIS = [dataset_api, track_api, gene_api]

api = Namespace('genomics', description="API Calls for accessing the NIAGADS Alzheimer's Genomics Database")

model = api.model('API Info', api_root_information)
parser = parsers.genome_build

@api.route('/')
@api.expect(parser)
class Genomics(Resource):
    @api.marshal_with(model, envelope='genomics')

    def get(self):
        args = parsers.parse_args()
        genomeBuild = args['assembly']
        resourceEndpoint = "genomics" if genomeBuild == 'GRCh38' else "genomics37"
        apiEndpoint = "/genomics" if genomeBuild == 'GRCh38' else "/genomics/?assembly=GRCh37"
        return {"endpoint": apiEndpoint,
                "resource_url": "https://www.niagads.org/" + resourceEndpoint,
                "organization": "NIAGADS", 
                "organization_url": "https://www.niagads.org", 
                "description": "API Calls for accessing the NIAGADS Alzheimer's Genomics Database (" + genomeBuild + ")"}
