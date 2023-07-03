''' api to retrieve all tracks associated with a dataset '''
import logging
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources.constants import ADSP_VARIANTS_ACCESSION
from shared_resources.db import db as genomicsdb
from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources.utils import extract_result_data

from shared_resources.schemas.track import metadata
from genomics.shared.schemas import metadata as genomicsdb_metadata, phenotype
from genomics.dataset.schemas import metadata as dataset_metadata

from genomics.dataset.models import table
from genomics.track.models import table as track_table

logger = logging.getLogger(__name__)

api = Namespace('genomics/dataset',
        description="retrieve dataset metadata, where a dataset is collection of one or more related tracks from the NIAGADS repository; a NIAGADS accession)")

# create response schema from the base metadata schema
metadata_schema = api.model('Dataset', metadata)
phenotypes_schema = api.model('Phenotype', phenotype)

# extend w/GenomicsDB - only fields
genomicsdb_metadata_schema = api.clone(
        'GenomicsDB Dataset', 
        metadata_schema, 
        genomicsdb_metadata,
        dataset_metadata
        #{'phenotypes': fields.Nested(phenotypes_schema, skip_none=True, desciption="clinical phenotypes", example="coming soon")}
)

@api.route('/<string:id>', doc={"description": "retrieve meta-data for specified dataset"})
@api.expect(parsers.genome_build)
class Dataset(Resource):
    @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    @api.doc(params={
            'id': 'unique dataset identifier or accession number in original datasource'
            })
    
    def get(self, id): 
        args = parsers.genome_build.parse_args()
        dataset = genomicsdb.one_or_404(
            statement=genomicsdb.select(table(args['assembly'])).filter_by(id=id),
            description=f"No database with accession # {id} found in the NIAGADS GenomicsDB."
        )
        
        return dataset

filter_parser = parsers.filters.copy()
filter_parser.replace_argument('type', help="type of dataset or track; what kind of information", 
        default="GWAS_sumstats", choices=["GWAS_sumstats"], required=True)
filter_parser = merge_parsers(filter_parser, parsers.genome_build)

@api.route('/', doc={"description": "retrieve meta-data for datasets by type"})
@api.expect(filter_parser)
class DatasetList(Resource):    
    @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    def get(self):
        args = filter_parser.parse_args()
        queryTable = table(args['assembly'])
        idMatch = "{}%".format("NG0")
        ignore = "{}%".format(ADSP_VARIANTS_ACCESSION)
        
        # TODO: add conditional based on type
        datasets = genomicsdb.session.execute(genomicsdb.select(queryTable)
                .filter(queryTable.id.like(idMatch) 
                        & not_(queryTable.id.like(ignore)))
                .order_by(queryTable.id))
        
        return extract_result_data(datasets)
