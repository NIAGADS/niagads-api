''' api to retrieve all tracks associated with a dataset '''
import logging

from flask_restx import Namespace, Resource, marshal, fields
from marshmallow import ValidationError
from shared_resources.parsers import arg_parsers as parsers, merge_parsers, add_boolean_arg
from shared_resources import constants, utils
from shared_resources.db import db

from filer.utils import make_request
from filer.track.schemas import metadata, biosample
from filer.track.models import get_track_count, get_filter_values, get_track_metadata, validate_track
from filer.parsers import filter_arg_parser

LOGGER = logging.getLogger(__name__)

SPAN_PARSER = merge_parsers(parsers.genome_build, parsers.span)
FILTER_PARSER = merge_parsers(parsers.genome_build, filter_arg_parser)
add_boolean_arg(FILTER_PARSER, "countOnly", "return number of tracks that match the filter criteria")
add_boolean_arg(FILTER_PARSER, "idsOnly", "return a list of track IDs that match the filter criteria")
# add_boolean_arg(FILTER_PARSER, "full", "return full metadata")

TRACK_FILTERS = list(constants.ALLOWABLE_FILER_TRACK_FILTERS.keys())

api = Namespace('filer/track',
        description="retrieve track metadata and data")

# create response schema from the base metadata schema
trackSchema = api.model('FILER Track', metadata)
biosampleSchema = api.model('BioSample', biosample)
# trackSchema = api.clone('FILER Track', trackSchema, 
#        {"biosample": fields.Nested(biosampleSchema, skip_none=True, desciption="biosample characteristics")})


@api.route('/<string:id>', doc={"description": "retrieve meta-data for specified track from FILER"})
@api.expect(parsers.genome_build)
class Track(Resource):
    @api.marshal_with(trackSchema, skip_none=True)
    @api.doc(params={'id': 'unique track identifier'})  
    def get(self, id): 
        args = parsers.genome_build.parse_args()
        return validate_track(id, args['assembly'], True)


@api.route('/', doc={"description": "retrieve meta-data for FILER tracks matching filter criteria"})
@api.expect(FILTER_PARSER)  
class TrackList(Resource):
    def get(self):
        args = FILTER_PARSER.parse_args()
        count = get_track_count(args)
        result = {"query_params": args, "num_matched_tracks": count }
        if args.countOnly:
            return result, 200
        
        if count > 1000:
            message = utils.error_message("More than 1000 tracks found matching the filter criteria, please add additional filters; pagination coming soon", errorType="result_too_large")
            result.update(message)
            return result, 200

        if args.idsOnly:
            result.update({"tracks": get_track_metadata(args)})
        else: # get the metadata
            # note @api.marshal_with is a convience wrapper for the marshal call
            result.update({"tracks": marshal(get_track_metadata(args), trackSchema)})
            
        return result, 200
    

@api.route('/<string:id>/overlaps', doc={"description": "get track data in the specified span"})
@api.expect(SPAN_PARSER)
class TrackOverlaps(Resource):
    @api.doc(params={'id': 'unique track identifier'})  
    def get(self, id,):
        args = SPAN_PARSER.parse_args()
        validate_track(id, args['assembly'], False)         # if not valid, returns an error
        try:
            span = utils.parse_span(args)
            if isinstance(span, dict):
                return span # error message
            return make_request("get_overlaps", {"id": id, "assembly": args['assembly'], "span": span})
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")
       
            
        



@api.route('/filter/<string:filterName>')
class Filter(Resource):
    @api.doc(params={'filterName': 
        'an aspect of the track metadata that can be used to filter for relevant tracks; allowable values: ' 
        + utils.to_string(TRACK_FILTERS, delim=", ")})
    def get(self, filterName):
        if filterName not in TRACK_FILTERS:
            return utils.error_message({"arg":"filterName", "bad_value": filterName, "valid_values": TRACK_FILTERS}, messageType="bad_arg")
        return get_filter_values(filterName)
    
        
        
# @api.route('/<string:id>', doc={"description": "retrieve meta-data for specified track from the NIAGADS GenomicsDB"})
# @api.expect(parsers.genome_build)
# class Track(Resource):
#     # @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
#     @api.doc(params={'id': 'unique track identifier'})
#     def get(self, id):

#         return response
