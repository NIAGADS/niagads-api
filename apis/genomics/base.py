from flask_restx import Namespace, Resource, fields
from schemas import api_root_information
from .entities import dataset_api

CHILD_APIS = [dataset_api]

api = Namespace(
    'genomics', description="API Calls for accessing the NIAGADS Alzheimer's Genomics Database")

model = api.model('BaseInfo', api_root_information)

@api.route('/about')
class Genomics(Resource):
    @api.marshal_with(model, envelope='genomics')
    def get(self):
        return {"endpoint": "/genomics",
                "resource_url": "https://www.niagads.org/genomics", 
                "organization": "NIAGADS", 
                "organization_url": "https://www.niagads.org", 
                "description": "API Calls for accessing the NIAGADS Alzheimer's Genomics Database"}
