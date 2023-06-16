from flask_restx import fields
from shared_resources.fields import GenomeBuild

feature_properties = {
    'feature_type': fields.String(description="feature type", required=True, example="gene"),
    'id': fields.String(description="Ensembl Identifier", required=True, example="ENSG00000130203"),
    'start': fields.Integer(description="start coordinate for gene", required=True, example=45409011),
    'end': fields.Integer(description="end coordinate for gene", required=True, example=45412650),
    'chromosome': fields.String(description="chromosome on which gene is located", required=True, example="chr19"),
    # 'assembly': GenomeBuild(description="reference genome build", required=True, example="GRCh38")
    'assembly': fields.String(description="reference genome build", required=True, example="GRCh38")
}

gene_properties = {
    'symbol': fields.String(description="Official gene symbol", required=True, example="APOE"),
    'transcript_count': fields.String(description="number of transcripts in this gene"),
    'exon_count': fields.String(description="number of exons in this gene") 
}

exon_properties = {
   'number': fields.Integer(description="exon number", required=True)
}

tanscript_properties = {
    'name': fields.String(description="transcript name", required=True),
    'canonical': fields.Boolean(description="flag indicating whether this is the canonical transcript for the gene")
}