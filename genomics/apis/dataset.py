''' api to retrieve all tracks associated with a dataset '''
from db import genomicsdb
from flask_restx import Namespace, Resource, fields
from shared_resources.schemas.dataset import metadata
from genomics.schemas.dataset import metadata as genomicsdb_metadata, phenotype
from genomics.models.tables.dataset import table
from shared_resources.fields import GenomeBuild



api = Namespace(
    'genomics/dataset', description="Retrieve dataset metadata (dataset = set of one or more tracks from the NIAGADS repository; a NIAGADS accession)")

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


@api.route('/<string:genome_build>/<string:id>', doc={"description": "retrieve meta-data for specified dataset"})
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
