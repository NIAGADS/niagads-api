''' api to retrieve all tracks associated with a dataset '''
import logging

from flask_restx import Namespace, Resource

from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources.urls import external as urls
from shared_resources.schemas.track import metadata

from filer.utils import make_request

logger = logging.getLogger(__name__)

api = Namespace('filer/track',
        description="retrieve track metadata and data")

# create response schema from the base metadata schema
metadata_schema = api.model('Track', metadata)

# extend w/FILER - only fields
filer_metadata_schema = api.clone(
        'FILER Track', 
        metadata_schema, 
        # filer_metadata,
        # track_metadata
       #{'phenotypes': fields.Nested(phenotypes_schema, skip_none=True, desciption="clinical phenotypes", example="coming soon")}
        )

@api.route('/<string:id>', doc={"description": "retrieve meta-data for specified track from the NIAGADS GenomicsDB"})
@api.expect(parsers.genome_build)
class Track(Resource):
    # @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    @api.doc(params={'id': 'unique track identifier'})
    def get(self, id):
        args = parsers.genome_build.parse_args()
        response = make_request('get_metadata', args)
        return response
