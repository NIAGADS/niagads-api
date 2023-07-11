''' api to get all tracks associated with a collection '''
import logging
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources.db import db as genomicsdb
from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources import utils, constants

from genomics.shared.schemas import base_metadata, phenotype
from genomics.collection.schemas import metadata as collection_metadata
from genomics.collection.models import table, validate_collection
from genomics.track.models import table as track_table
from genomics.track.schemas import metadata as track_metadata

logger = logging.getLogger(__name__)

api = Namespace('genomics/collection',
        description="get collection metadata; a collection is a set of one or more related tracks, usually linked to a publication, from the NIAGADS repository; a NIAGADS accession)")

# create response schema from the base metadata schema
baseSchema = api.model('Metadata', base_metadata)
phenotypeSchema = api.model('Phenotype', phenotype)
trackSchema = api.clone('GenomicsDB Track', baseSchema, track_metadata)
collectionSchema = api.clone('GenomicsDB Collection', baseSchema, collection_metadata)
#{'phenotypes': fields.Nested(phenotypes_schema, skip_none=True, desciption="clinical phenotypes", example="coming soon")}

@api.route('/<string:id>', doc={"description": "get meta-data for specified collection"})
@api.expect(parsers.genome_build)
class Collection(Resource):
    @api.marshal_with(collectionSchema, skip_none=True)
    @api.doc(params={
            'id': 'unique collection identifier or accession number in original datasource'
            })
    
    def get(self, id): 
        args = parsers.genome_build.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])     
            collection = validate_collection(id, genomeBuild, True)        
            return collection
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")

filterParser = parsers.filters.copy()
filterParser.replace_argument('dataType', help="type of data or analysis output type",
        default="GWAS_sumstats", choices=["GWAS_sumstats"], required=True)
argParser = merge_parsers(filterParser, parsers.genome_build)
@api.route('/', doc={"description": "get meta-data for collections by type"})
@api.expect(argParser)
class CollectionList(Resource):    
    @api.marshal_with(collectionSchema, skip_none=True)
    def get(self):
        args = argParser.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])    

            queryTable = table(genomeBuild)
            idMatch = "{}%".format("NG0")
            ignore = "{}%".format(constants.ADSP_VARIANTS_ACCESSION)
            
            # TODO: add conditional based on type
            collections = genomicsdb.session.execute(genomicsdb.select(queryTable)
                    .filter(queryTable.id.like(idMatch) 
                            & not_(queryTable.id.like(ignore)))
                    .order_by(queryTable.id))
            
            return utils.extract_result_data(collections)

        except ValidationError as err: 
            return utils.error_message(str(err), errorType="validation_error")


@api.route('/<string:id>/tracks', doc={"description": "get meta-data for tracks associated with the specified collection"})
@api.expect(parsers.genome_build)
class CollectionTracks(Resource):
    @api.marshal_with(trackSchema, skip_none=True)
    @api.doc(params={
            'id': 'unique collection identifier or accession number in original datasource'
            })
    
    def get(self, id): 
        args = parsers.genome_build.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])
            validate_collection(id, genomeBuild, False)     
            queryTable = track_table(genomeBuild)
            tracks = genomicsdb.session.execute(genomicsdb.select(queryTable)
                    .filter_by(dataset_accession=id)
                    .order_by(queryTable.id))
            return utils.extract_result_data(tracks)
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")
    