''' api to get all tracks associated with a gene or gene subfeature '''
from flask_restx import Namespace, Resource
from sqlalchemy import literal
from marshmallow import ValidationError

from shared_resources.db import db as genomicsdb
from shared_resources.schemas.gene_features import feature_properties, gene_properties
from shared_resources.parsers import arg_parsers as parsers, merge_parsers
from shared_resources import utils

from genomics.shared.schemas import gene as genomicsdb_gene_properties
from genomics.gene.models import table

api = Namespace('genomics/gene', description="get gene annotations from the NIAGADS GenomicsDB")

# create response schema from the base gene schema
featureSchema = api.model('Feature', feature_properties)
geneSchema = api.clone('Gene', featureSchema, gene_properties, genomicsdb_gene_properties)

@api.route('/<string:id>', doc={"description": "get basic identifying annotation for the specified gene"})
@api.expect(parsers.genome_build)
class Gene(Resource):
    @api.marshal_with(geneSchema, skip_none=True)
    @api.doc(
        params={
            'id': 'gene id: Ensembl ID, NCBI Gene (Entrez) ID or official gene symbol; queries against symbols will be case sensitive and match official symbols only'
        }
    )
    # genome_build:str = Route(default="GRCh38", pattern="GRCh(38|37)")):
    def get(self, id):
        args = parsers.genome_build.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])
            queryTable = table(genomeBuild)
            gene = genomicsdb.one_or_404(statement=genomicsdb.select(queryTable, 
                    literal("gene").label("feature_type"),
                    literal(args['assembly']).label("assembly"))
                    .filter((queryTable.gene_symbol == id) | (queryTable.source_id == id) | (queryTable.annotation['entrez_id'].astext == id)),
                    description=f"No gene with identifier {id} found in the NIAGADS GenomicsDB for {args['assembly']}.")
            return gene
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")
    

argParser = merge_parsers(parsers.id_enum, parsers.genome_build)
@api.route('/', doc={"description": "get basic identifying annotation for a list one or more genes"})
@api.expect(argParser)
class GeneList(Resource):
    @api.marshal_with(geneSchema, skip_none=True, as_list=True)
    def get(self):
        args = argParser.parse_args()
        try:
            genomeBuild = utils.validate_assembly(args['assembly'])
            queryTable = table(genomeBuild)
            genes = genomicsdb.session.execute(genomicsdb.select(queryTable, 
                    literal("gene").label("feature_type"), 
                    literal(args['assembly']).label("assembly"))
                    .filter(queryTable.gene_symbol.in_(args.id) 
                            | queryTable.source_id.in_(args['id']) 
                            | queryTable.annotation['entrez_id'].astext.in_(args['id'])).order_by(queryTable.source_id))
            return utils.extract_result_data(genes, hasLiterals=True)
        except ValidationError as err:
            return utils.error_message(str(err), errorType="validation_error")
    
    
# /gene/genome_build?ids=
# /gene/genome_build?ids=
# /gene/genome_build/id/function
# /gene/genome_build/id/pathway
# /gene/genome_build/id/variants/impact
# /gene/genome_build/id/variants/gwas?flank=<x>&adOnly

# exons / transcripts / introns?

# /gene/genome_build/overlap/(span=|chr-start-end)&featureType=all/exon/intron/cds/utr&geneType --> all genes and gene subfeatures in a span

