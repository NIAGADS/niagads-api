from flask_restx import Api

from apis.genomics.base import api as genomics_api

api = Api(
    title='NIAGADS API',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(genomics_api)
# api.add_namespace(ns2)
# ...
# api.add_namespace(nsX)