''' api to retrieve all tracks associated with a dataset '''
from db import genomicsdb
from flask_restx import Namespace, Resource, fields, reqparse
from shared_resources.schemas.gene_features import feature_properties, gene_properties
from shared_resources.parsers import parser
from genomics.schemas.gene import gene_extended_properties
from genomics.models.tables.gene import table


api = Namespace('genomics/gene', description="retrieve gene annotations from the NIAGADS GenomicsDB")

# create response schema from the base gene schema
feature_schema = api.model('Feature', feature_properties)
gene_base_schema = api.clone('Gene', feature_schema, gene_properties)
genomicsdb_gene_schema = api.clone('GenomicsDB Gene', gene_base_schema, gene_extended_properties)


@api.route('/<string:genome_build>/<string:id>', doc={"description": "get basic identifying annotation for the specified gene"})
class Gene(Resource):
    @api.marshal_with(genomicsdb_gene_schema, skip_none=True)
    @api.doc(
        params={
            'id': 'gene id: Ensembl ID, NCBI Gene (Entrez) ID or official gene symbol; queries against symbols will be case sensitive and match official symbols only',
            'genome_build': 'assembly; one of GRCh38 or GRCh37'
        }
    )
    # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
    def get(self, id, genome_build):
        queryTable = table(genome_build)
        gene = genomicsdb.one_or_404(statement=genomicsdb.select(queryTable, ("gene").label("feature_type"))
                .filter((queryTable.gene_symbol == id) | (queryTable.source_id == id) | (queryTable.annotation['entrez_id'] == id)),
                description=f"No gene with identifier {id} found in the NIAGADS GenomicsDB for {genome_build}.")
        return gene
    



@api.route('/<string:genome_build>', doc={"description": "get basic identifying annotation for a list of genes"})
@api.expect(parser.enum_id)
class GeneList(Resource):
    @api.marshal_list_with(genomicsdb_gene_schema, skip_none=True)
    def get(self, genome_build):
        args = parser.enum_id.parse_args()
        queryTable = table(genome_build)
        genes = genomicsdb.select(queryTable, ("gene").label("feature_type")) \
                .filter(queryTable.gene_symbol.in_(args.id) | queryTable.source_id.in_(args['id']) | queryTable.annotation['entrez_id'].in_(args['id'])) 
        return genes
    
    
# /gene/genome_build?ids=
# /gene/genome_build?ids=
# /gene/genome_build/id/function
# /gene/genome_build/id/pathway
# /gene/genome_build/id/variants/impact
# /gene/genome_build/id/variants/gwas?flank=<x>&adOnly

# exons / transcripts / introns?

# /gene/genome_build/overlap/(span=|chr-start-end)&featureType=all/exon/intron/cds/utr&geneType --> all genes and gene subfeatures in a span

