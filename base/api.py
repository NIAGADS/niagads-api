from flask_restx import Api

from genomics import genomics_api as genomics_api, genomics_api_children

api = Api(
    title='NIAGADS API',
    version='1.0',
    description='API for accessing NIAGADS resources',
    # All API metadatas
)

api.add_namespace(genomics_api)
for ns in genomics_api_children:
    api.add_namespace(ns)