from flask_restx import fields

gene_basic_properties = {
    'id': fields.String(description="Ensembl Identifier", required=True, example="ENSG00000130203"),
    'symbol': fields.String(description="Official gene symbol", required=True, example="APOE"),
    'start': fields.Integer(description="start coordinate for gene", required=True, example=45409011),
    'end': fields.Integer(description="end coordinate for gene", required=True, example=45412650),
    'chromosome': fields.String(description="chromosome on which gene is located", required=True, example="chr19"),
}
