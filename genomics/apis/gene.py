''' api to retrieve all tracks associated with a dataset '''
from db import genomicsdb
from flask_restx import Namespace, Resource, fields
from shared_resources.schemas.gene import gene_basic_properties
from genomics.schemas.gene import gene_extended_properties
from genomics.models.tables.gene import table

api = Namespace('genomics/gene',
        description="retrieve gene annotations from the NIAGADS GenomicsDB")

# create response schema from the base gene schema
gene_base_schema = api.model('Gene', gene_basic_properties)
genomicsdb_gene_schema = api.clone('GenomicsDB Gene', gene_base_schema, gene_extended_properties)


@api.route('/<string:genome_build>/<string:id>', doc={"description": "get basic identifying annotation for the specified gene"})
class Gene(Resource):
    @api.marshal_with(genomicsdb_gene_schema, skip_none=True)
    @api.doc(
        params={
            'id': 'gene id: Ensembl ID, NCBI Gene (Entrez) ID or official gene symbol; queries against symobls will be for exact matches only',
            'genome_build': 'assembly; one of GRCh38 or GRCh37'
        }
    )
    # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
    def get(self, id, genome_build):
        queryTable = table(genome_build)
        gene = genomicsdb.one_or_404(statement=genomicsdb.select(queryTable)
                .filter((queryTable.gene_symbol == id) | (queryTable.source_id == id) | (queryTable.annotation['entrez_id'] == id)),
                description=f"No gene with identifier {id} found in the NIAGADS GenomicsDB for {genome_build}.")

        return gene

# /gene/genome_build?ids=
# /gene/genome_build?ids=
# /gene/genome_build/id/function
# /gene/genome_build/id/pathway
# /gene/genome_build/id/variants/impact
# /gene/genome_build/id/variants/gwas?flank=<x>&adOnly

# exons / transcripts / introns?

# /gene/genome_build/overlap/(span=|chr-start-end)&featureType=all/exon/intron/cds/utr&geneType --> all genes and gene subfeatures in a span

# /genome_build/ids=?
# @api.route('/<string:genome_build>/<string:id>',
#        doc={"description": "get basic identifying annotation for the specified gene"})
# class GeneList(Resource):
