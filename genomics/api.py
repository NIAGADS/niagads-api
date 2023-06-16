from flask_restx import Namespace, Resource, fields
from shared_resources.schemas.about import api_root_information
from shared_resources.fields.genome_build import GenomeBuild

# child APIs
from genomics.gene.api import api as gene_api
from genomics.dataset.api import api as dataset_api

CHILD_APIS = [dataset_api, gene_api]

api = Namespace('genomics/<genome_build>', description="API Calls for accessing the NIAGADS Alzheimer's Genomics Database")
model = api.model('API Info', api_root_information)
@api.doc(params={'genome_build': 'assembly; one of GRCh38 or GRCh37'})
@api.route('/')
class Genomics(Resource):
    @api.marshal_with(model, envelope='genomics')

    def get(self, genome_build):
        genomeBuild = GenomeBuild().deserialize(genome_build)
        endpoint = "genomics" if genomeBuild == 'GRCh38' else "genomics37"
        return {"endpoint": "/" + genomeBuild + "/genomics",
                "resource_url": "https://www.niagads.org/" + endpoint,
                "organization": "NIAGADS", 
                "organization_url": "https://www.niagads.org", 
                "description": "API Calls for accessing the NIAGADS Alzheimer's Genomics Database (" + genomeBuild + ")"}
