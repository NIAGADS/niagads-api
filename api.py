from flask_restx import Api
from config.utils import get_version
from genomics import genomics_api, genomics_api_children
from filer import filer_api, filer_api_children


version = get_version()

api = Api(
    title='NIAGADS API',
    version=version,
    description='API for accessing NIAGADS knowledgebases',
    doc='/doc/'
)

api.add_namespace(genomics_api)
for ns in genomics_api_children:
   api.add_namespace(ns)
    
api.add_namespace(filer_api)
for ns in filer_api_children:
    api.add_namespace(ns)

