''' api to retrieve all tracks associated with a gene or gene subfeature '''
from flask_restx import Namespace, Resource
from sqlalchemy import literal

from shared_resources.db import genomicsdb
from shared_resources.schemas.gene_features import feature_properties, gene_properties
from shared_resources.parsers import parsers, merge_parsers
from shared_resources.utils import extract_result_data

from genomics.gene.schemas import gene_extended_properties
from genomics.gene.models import table


api = Namespace('genomics/gene', description="retrieve gene annotations from the NIAGADS GenomicsDB")

# create response schema from the base gene schema
feature_schema = api.model('Feature', feature_properties)
gene_base_schema = api.clone('Gene', feature_schema, gene_properties)
genomicsdb_gene_schema = api.clone('GenomicsDB Gene', gene_base_schema, gene_extended_properties)


@api.route('/<string:id>', doc={"description": "get basic identifying annotation for the specified gene"})
@api.expect(parsers.genome_build)
class Gene(Resource):
    @api.marshal_with(genomicsdb_gene_schema, skip_none=True)
    @api.doc(
        params={
            'id': 'gene id: Ensembl ID, NCBI Gene (Entrez) ID or official gene symbol; queries against symbols will be case sensitive and match official symbols only'
        }
    )
    # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
    def get(self, id):
        args = parsers.genome_build.parse_args()
        queryTable = table(args['assembly'])
        gene = genomicsdb.one_or_404(statement=genomicsdb.select(queryTable, 
                literal("gene").label("feature_type"),
                literal(args['assembly']).label("assembly"))
                .filter((queryTable.gene_symbol == id) | (queryTable.source_id == id) | (queryTable.annotation['entrez_id'].astext == id)),
                description=f"No gene with identifier {id} found in the NIAGADS GenomicsDB for {args['assembly']}.")
        return gene
    


lookup_parser = merge_parsers(parsers.id_enum, parsers.genome_build)
@api.route('/', doc={"description": "get basic identifying annotation for a list one or more genes"})
@api.expect(lookup_parser)
class GeneList(Resource):
    @api.marshal_with(genomicsdb_gene_schema, skip_none=True, as_list=True)
    def get(self):
        args = lookup_parser.parse_args()
        queryTable = table(args['assembly'])
        genes = genomicsdb.session.execute(genomicsdb.select(queryTable, 
                literal("gene").label("feature_type"), 
                literal(args['assembly']).label("assembly"))
                .filter(queryTable.gene_symbol.in_(args.id) 
                        | queryTable.source_id.in_(args['id']) 
                        | queryTable.annotation['entrez_id'].astext.in_(args['id'])).order_by(queryTable.source_id))
        return extract_result_data(genes)
    
    
# /gene/genome_build?ids=
# /gene/genome_build?ids=
# /gene/genome_build/id/function
# /gene/genome_build/id/pathway
# /gene/genome_build/id/variants/impact
# /gene/genome_build/id/variants/gwas?flank=<x>&adOnly

# exons / transcripts / introns?

# /gene/genome_build/overlap/(span=|chr-start-end)&featureType=all/exon/intron/cds/utr&geneType --> all genes and gene subfeatures in a span

