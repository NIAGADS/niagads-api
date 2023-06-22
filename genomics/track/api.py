''' api to retrieve all tracks associated with a dataset '''
import logging
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources.constants import ADSP_VARIANTS_ACCESSION
from shared_resources.db import genomicsdb
from shared_resources.parsers import arg_parsers as parsers, merge_parsers

from shared_resources.utils import extract_result_data

from shared_resources.schemas.track import metadata
from genomics.metadata.schemas import metadata as genomicsdb_metadata, phenotype
from genomics.track.schemas import metadata as track_metadata

from genomics.track.models import table

logger = logging.getLogger(__name__)

api = Namespace('genomics/track',
        description="retrieve track metadata and data")

# create response schema from the base metadata schema
metadata_schema = api.model('Track', metadata)
phenotypes_schema = api.model('Phenotype', phenotype)

# extend w/GenomicsDB - only fields
genomicsdb_metadata_schema = api.clone(
        'GenomicsDB Track', 
        metadata_schema, 
        genomicsdb_metadata,
        track_metadata
       #{'phenotypes': fields.Nested(phenotypes_schema, skip_none=True, desciption="clinical phenotypes", example="coming soon")}
        )

@api.route('/<string:id>', doc={"description": "retrieve meta-data for specified track from the NIAGADS GenomicsDB"})
@api.expect(parsers.genome_build)
class Track(Resource):
    @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    @api.doc(params={'id': 'unique track identifier'})
   
    def get(self, id): # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
        args = parsers.genome_build.parse_args()
        dataset = genomicsdb.one_or_404(
            statement=genomicsdb.select(table(args['assembly'])).filter_by(id=id),
            description=f"No track with id {id} found in the NIAGADS GenomicsDB."
        )
        
        return dataset

filter_parser = parsers.filters.copy()
filter_parser.replace_argument('type', help="type of track; what kind of information", default="GWAS_sumstats", choices=["GWAS_sumstats"], required=True)
filter_parser = merge_parsers(filter_parser, parsers.genome_build)
@api.route('/', doc={"description": "retrieve meta-data for tracks by type"})
@api.expect(filter_parser)
class TrackList(Resource):    

    @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    def get(self):
        args = filter_parser.parse_args()
        
        queryTable = table(args['assembly'])
        idMatch = "{}%".format("NG0")
        ignore = "{}%".format(ADSP_VARIANTS_ACCESSION)
         
        # TODO: add conditional based on type
        tracks = genomicsdb.session.execute(genomicsdb.select(queryTable)
                .filter(queryTable.id.like(idMatch) 
                        & not_(queryTable.id.like(ignore)))
                .order_by(queryTable.id))
        
        return extract_result_data(tracks)
