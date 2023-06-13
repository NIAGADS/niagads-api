from flask_restx import fields

feature_properties = {
    'feature_type': fields.String(description="feature type", required=True, example="gene"),
    'id': fields.String(description="Ensembl Identifier", required=True, example="ENSG00000130203"),
    'start': fields.Integer(description="start coordinate for gene", required=True, example=45409011),
    'end': fields.Integer(description="end coordinate for gene", required=True, example=45412650),
    'chromosome': fields.String(description="chromosome on which gene is located", required=True, example="chr19"),
}

gene_properties = {
    'symbol': fields.String(description="Official gene symbol", required=True, example="APOE"),
    'transcript_count': fields.String(description="number of transcripts in this gene"),
    'exon_count': fields.String(description="number of exons in this gene") 
}

exon_properties = {
   
}

tanscript_properties = {
    'name': fields.String(description="transcript name", required=True)
}