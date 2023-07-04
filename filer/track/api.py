''' api to retrieve all tracks associated with a dataset '''
import logging

from flask_restx import Namespace, Resource

from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources.constants import URLS
from shared_resources.schemas.track import metadata
from shared_resources.db import db

from filer.utils import make_request
from filer.track.models import Track, get_track_count

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

@api.route('/')
@api.expect(parsers.genome_build)
class Track(Resource):
    def get(self):
        count = get_track_count(None)
        return {"count": count }

# @api.route('/<string:id>', doc={"description": "retrieve meta-data for specified track from the NIAGADS GenomicsDB"})
# @api.expect(parsers.genome_build)
# class Track(Resource):
#     # @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
#     @api.doc(params={'id': 'unique track identifier'})
#     def get(self, id):

#         return response
