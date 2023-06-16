''' api to retrieve all tracks associated with a dataset '''
import logging
from flask_restx import Namespace, Resource
from sqlalchemy import not_

from shared_resources.constants import ADSP_VARIANTS_ACCESSION
from shared_resources.db import genomicsdb
from shared_resources.parsers import parser
from shared_resources.schemas.dataset import metadata
from shared_resources.utils import extract_result_data

from genomics.dataset.schemas import metadata as genomicsdb_metadata, phenotype
from genomics.dataset.models import table

logger = logging.getLogger(__name__)

api = Namespace('genomics/<genome_build>/dataset',
        description="Retrieve dataset metadata (dataset = set of one or more tracks from the NIAGADS repository; a NIAGADS accession)")

# create response schema from the base metadata schema
metadata_schema = api.model('Dataset', metadata)
phenotypes_schema = api.model('Phenotype', phenotype)

# extend w/GenomicsDB - only fields
genomicsdb_metadata_schema = api.clone(
        'GenomicsDB Dataset', 
        metadata_schema, 
        genomicsdb_metadata,
       #{'phenotypes': fields.Nested(phenotypes_schema, desciption="clinical phenotypes", example="coming soon")}
        )

@api.route('/<string:id>', doc={"description": "retrieve meta-data for specified dataset"})
class Dataset(Resource):
    @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    @api.doc(params={
            'id': 'unique dataset identifier or accession number in original datasource',
            'genome_build': 'assembly; one of GRCh38 or GRCh37'
            })
   
    def get(self, id, genome_build): # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
        dataset = genomicsdb.one_or_404(
            statement=genomicsdb.select(table(genome_build)).filter_by(accession=id),
            description=f"No database with accession # {id} found in the NIAGADS GenomicsDB."
        )
        
        return dataset

fparser = parser.filters.copy()
fparser.replace_argument('type', help="type of dataset or track; what kind of information", default="GWAS_sumstats", choices=["GWAS_sumstats"], required=True)
@api.route('/', doc={"description": "retrieve meta-data for datasets by type"})
@api.expect(fparser)
class DatasetList(Resource):    

    @api.marshal_with(genomicsdb_metadata_schema, skip_none=True)
    def get(self, genome_build):
        args = fparser.parse_args()
        queryTable = table(genome_build)
        idMatch = "{}%".format("NG0")
        ignore = "{}%".format(ADSP_VARIANTS_ACCESSION)
        logger.info("Retrieving datasets with idMatch = " + idMatch + " and type = " + args['type'])
        
        # TODO: add conditional based on type
        datasets = genomicsdb.session.execute(genomicsdb.select(queryTable)
                .filter(queryTable.accession.like(idMatch) 
                        & not_(queryTable.accession.like(ignore)))
                .order_by(queryTable.accession))
        
        return extract_result_data(datasets)
