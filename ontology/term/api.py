''' API for ontology terms '''
import logging

from flask_restx import Namespace, Resource, marshal, fields
from marshmallow import ValidationError
from shared_resources.parsers import arg_parsers as parsers, merge_parsers, add_boolean_arg

from shared_resources.db import db


LOGGER = logging.getLogger(__name__)


api = Namespace('ontology/term',
        description="lookup ontology terms")

# create response schema from the base metadata schema

#@api.route('/<string:id>', doc={"description": "get ADVP curated AD/ADRD-associations for the selected variant"})
#class Variant(Resource):
    #@api.marshal_with(variantSchema, skip_none=True)
#    @api.doc(params={'id': 'dbSNP refSNP (rs) identifier'})  
#    def get(self, id): 
#        return validate_variant(id, returnRecord=True)

