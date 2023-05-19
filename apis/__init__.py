from flask_restx import Api

from apis.genomics.base import api as genomics_api #, CHILD_APIS as genomics_api_children
from apis.genomics.entities import dataset_api

api = Api(
    title='NIAGADS API',
    version='1.0',
    description='API for accessing NIAGADS resources',
    # All API metadatas
)

api.add_namespace(genomics_api)
api.add_namespace(dataset_api)
# for ns in genomics_api_children:
#     api.add_namespace(ns)
# api.add_namespace(ns2)
# ...
# api.add_namespace(nsX)