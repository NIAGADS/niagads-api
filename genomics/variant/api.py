''' api to retrieve all tracks associated with a dataset '''
import logging
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources import constants, utils
from shared_resources.db import db as genomicsdb
from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources.utils import extract_result_data

from genomics.variant.models import validate_variant, get_variant

logger = logging.getLogger(__name__)

api = Namespace('genomics/variant',
        description="lookup one or variants by id or region")

# create response schema from the base metadata schema

@api.route('/<string:id>', doc={"description": "get annotations for specified variant"})
@api.expect(parsers.genome_build)
class Variant(Resource):
    @api.doc(params={'id': 'refSnpId or chrN:pos:ref:alt, where chrN is one of 1..22,X,Y,M'})
    def get(self, id):
        args = parsers.genome_build.parse_args()
        result = get_variant(args['assembly'], id, single=True)
        if 'message' in result:
            return result, 404
        return result
    
argParser = merge_parsers(parsers.genome_build, parsers.id)
@api.route('/', doc={"description": "get annotations for specified variant"})
@api.expect(parsers.genome_build)
class VariantList(Resource):
    def get(self):
        args = argParser.parse_args(args['assembly'], args['id'])
        result = get_variant(args), 200
        return result