''' api to retrieve all tracks associated with a dataset '''
from db import genomicsdb
from flask_restx import Namespace, Resource, fields
from sqlalchemy import or_, text
from genomics.schemas.gene import gene as gene_model
from genomics.models.tables import Gene_GRCh37, Gene_GRCh38
from shared_resources.fields import GenomeBuild

api = Namespace(
    'genomics/gene', description="retrieve gene annotations from the NIAGADS GenomicsDB")

# create response schema from the base metadata schema
gene_schema = api.model('Gene', gene_model)

@api.route('/<string:genome_build>/<string:id>', doc={"description": "get identifying annotation for the specified gene"})
class Genomics(Resource):
    @api.marshal_with(gene_schema, skip_none=True)
    @api.doc(params={
            'id': 'gene id: Ensembl ID or official gene symbol; queries against symobls will be for exact matches only',
            'genome_build': 'assembly; one of GRCh38 or GRCh37'
            })
   
    def get(self, id, genome_build): # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
        bind_db = GenomeBuild().deserialize(genome_build)
        table = Gene_GRCh38 if bind_db == 'GRCh38' else Gene_GRCh37
        gene = genomicsdb.one_or_404(
            statement=genomicsdb.select(table)
                .filter_by(gene_symbol=id),
            description=f"No gene with identifier # {id} found in the NIAGADS GenomicsDB for {genome_build}."
        )

        return gene
