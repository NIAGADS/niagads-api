''' api to retrieve all tracks associated with a dataset '''
import logging
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources import constants, utils
from shared_resources.db import db as genomicsdb
from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources.utils import extract_result_data

from genomics.shared.schemas import base_metadata, phenotype
from genomics.track.schemas import metadata as track_metadata

from genomics.track.models import table, validate_track

logger = logging.getLogger(__name__)

api = Namespace('genomics/track',
        description="get track metadata and data")

# create response schema from the base metadata schema
baseSchema = api.model('Metadata', base_metadata)
phenotypeSchema = api.model('Phenotype', phenotype)
trackSchema = api.clone('GenomicsDB Track', baseSchema, track_metadata)
#{'phenotypes': fields.Nested(phenotypeSchema, skip_none=True, desciption="clinical phenotypes", example="coming soon")}


@api.route('/<string:id>', doc={"description": "get meta-data for specified track from the NIAGADS GenomicsDB"})
@api.expect(parsers.genome_build)
class Track(Resource):
    @api.marshal_with(trackSchema, skip_none=True)
    @api.doc(params={'id': 'unique track identifier'})
   
    def get(self, id): # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
        args = parsers.genome_build.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])
            dataset = validate_track(id, genomeBuild, True)
        
            return dataset
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")


filterParser = parsers.filters.copy()
filterParser.replace_argument('dataType', help="type of data or analysis output type",
        default="GWAS_sumstats", choices=["GWAS_sumstats"], required=True)
filterParser = merge_parsers(filterParser, parsers.genome_build)
@api.route('/', doc={"description": "get meta-data for tracks by type"})
@api.expect(filterParser)
class TrackList(Resource):    
    @api.marshal_with(trackSchema, skip_none=True)
    def get(self):
        args = filterParser.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])
            queryTable = table(genomeBuild)
            idMatch = "{}%".format("NG0")
            ignore = "{}%".format(constants.ADSP_VARIANTS_ACCESSION)
            
            # TODO: add conditional based on type
            tracks = genomicsdb.session.execute(genomicsdb.select(queryTable)
                    .filter(queryTable.id.like(idMatch) 
                            & not_(queryTable.id.like(ignore)))
                    .order_by(queryTable.id))
            
            return extract_result_data(tracks)
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")
