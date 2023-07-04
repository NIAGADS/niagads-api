''' api to retrieve all tracks associated with a dataset '''
import logging

from flask_restx import Namespace, Resource

from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources import constants, utils
from shared_resources.db import db

from filer.utils import make_request
from filer.track.schemas import metadata
from filer.track.models import Track, get_track_count, get_filter_values
from filer.parsers import filter_arg_parser

logger = logging.getLogger(__name__)

TRACK_FILTERS = list(constants.ALLOWABLE_FILER_TRACK_FILTERS.keys())

api = Namespace('filer/track',
        description="retrieve track metadata and data")

# create response schema from the base metadata schema
trackSchema = api.model('FILER Track', metadata)

argParser = merge_parsers(parsers.genome_build, filter_arg_parser)
@api.route('/', doc={"description": "retrieve meta-data for FILER tracks matching filter criteria"})
@api.expect(argParser)      
class Track(Resource):
    def get(self):
        args = argParser.parse_args()
        count = get_track_count(args)
        return {"count": count }

@api.route('/filter/<string:filterName>')
class Filter(Resource):
    @api.doc(params={'filterName': 
        'an aspect of the track metadata that can be used to filter for relevant tracks; allowable values: ' 
        + utils.to_string(TRACK_FILTERS, delim=", ")})
    def get(self, filterName):
        if filterName not in TRACK_FILTERS:
            return utils.error_message("filterName", filterName, TRACK_FILTERS)
        return get_filter_values(filterName)
    
        
        
# @api.route('/<string:id>', doc={"description": "retrieve meta-data for specified track from the NIAGADS GenomicsDB"})
# @api.expect(parsers.genome_build)
# class Track(Resource):
#     # @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
#     @api.doc(params={'id': 'unique track identifier'})
#     def get(self, id):

#         return response
