''' api to ADVP variants '''
import logging

from flask_restx import Namespace, Resource, marshal, fields
from marshmallow import ValidationError
from shared_resources.parsers import arg_parsers as parsers, merge_parsers, add_boolean_arg
from shared_resources import constants, utils
from shared_resources.db import db
from advp.variant.models import validate_variant
from advp.utils import make_request, clean_response

LOGGER = logging.getLogger(__name__)


api = Namespace('advp/variant',
        description="get variants from the ADVP, with genome-wide AD/ADRD-associations curated from AD-relevant publications")

# create response schema from the base metadata schema
# variantSchema = api.model('ADVP Variant', variant)

@api.route('/', doc={"description":"get summary list of all ADVP variants"})
class VariantList(Resource):
    def get(self):
        response = make_request("variants/get_variants")
        if 'message' in response:
            return response
        else:
            return [ clean_response(v) for v in response] 
        


#@api.route('/<string:id>', doc={"description": "get ADVP curated AD/ADRD-associations for the selected variant"})
#class Variant(Resource):
    #@api.marshal_with(variantSchema, skip_none=True)
#    @api.doc(params={'id': 'dbSNP refSNP (rs) identifier'})  
#    def get(self, id): 
#        return validate_variant(id, returnRecord=True)

