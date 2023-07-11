''' api to ADVP variants '''
import logging

from flask_restx import Namespace, Resource, marshal, fields
from marshmallow import ValidationError
from shared_resources.parsers import arg_parsers as parsers, merge_parsers, add_boolean_arg
from shared_resources import constants, utils
from shared_resources.db import db
from advp.variant.models import validate_variant

LOGGER = logging.getLogger(__name__)


api = Namespace('advp/variant',
        description="get variants from the ADVP, with genome-wide AD/ADRD-associations curated from AD-relevant publications")

# create response schema from the base metadata schema
variantSchema = api.model('ADVP Variant', variant)

@api.route('/<string:id>', doc={"description": "get ADVP curated AD/ADRD-associations for the selected variant"})
@api.expect(parsers.genome_build)
class Track(Resource):
    @api.marshal_with(variantSchema, skip_none=True)
    @api.doc(params={'id': 'unique track identifier'})  
    def get(self, id): 
        return validate_variant(id, returnRecord=True)

