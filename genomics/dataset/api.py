''' api to retrieve all tracks associated with a dataset '''
import logging
from marshmallow import ValidationError
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources.db import db as genomicsdb
from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources import utils, constants

from genomics.shared.schemas import base_metadata, phenotype
from genomics.dataset.schemas import metadata as dataset_metadata

from genomics.dataset.models import table
from genomics.track.models import table as track_table
from genomics.track.schemas import metadata as track_metadata

logger = logging.getLogger(__name__)

api = Namespace('genomics/dataset',
        description="retrieve dataset metadata, where a dataset is collection of one or more related tracks from the NIAGADS repository; a NIAGADS accession)")

# create response schema from the base metadata schema
baseSchema = api.model('Metadata', base_metadata)
phenotypeSchema = api.model('Phenotype', phenotype)
trackSchema = api.clone('GenomicsDB Track', baseSchema, track_metadata)
datasetSchema = api.clone('GenomicsDB Dataset', baseSchema, dataset_metadata)
#{'phenotypes': fields.Nested(phenotypes_schema, skip_none=True, desciption="clinical phenotypes", example="coming soon")}

@api.route('/<string:id>', doc={"description": "retrieve meta-data for specified dataset"})
@api.expect(parsers.genome_build)
class Dataset(Resource):
    @api.marshal_with(datasetSchema, skip_none=True)
    @api.doc(params={
            'id': 'unique dataset identifier or accession number in original datasource'
            })
    
    def get(self, id): 
        args = parsers.genome_build.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])     
            dataset = genomicsdb.one_or_404(
                statement=genomicsdb.select(table(genomeBuild)).filter_by(id=id),
                description=f"No database with accession # {id} found in the NIAGADS GenomicsDB."
            )
        
            return dataset
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")

filterParser = parsers.filters.copy()
filterParser.replace_argument('type', help="type of dataset or track; what kind of information", 
        default="GWAS_sumstats", choices=["GWAS_sumstats"], required=True)
argParser = merge_parsers(filterParser, parsers.genome_build)
@api.route('/', doc={"description": "retrieve meta-data for datasets by type"})
@api.expect(argParser)
class DatasetList(Resource):    
    @api.marshal_with(datasetSchema, skip_none=True)
    def get(self):
        args = argParser.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])    

            queryTable = table(genomeBuild)
            idMatch = "{}%".format("NG0")
            ignore = "{}%".format(constants.ADSP_VARIANTS_ACCESSION)
            
            # TODO: add conditional based on type
            datasets = genomicsdb.session.execute(genomicsdb.select(queryTable)
                    .filter(queryTable.id.like(idMatch) 
                            & not_(queryTable.id.like(ignore)))
                    .order_by(queryTable.id))
            
            return utils.extract_result_data(datasets)

        except ValidationError as err: 
            return utils.error_message(str(err), errorType="validation_error")
