from flask_restx import fields
from shared_resources.utils import extract_json_value

# TODO link outs

gene = {
    'id': fields.String(description="Ensembl Identifier", required=True),
    'symbol': fields.String(description="Official gene  symbol", required=True),
    'name': fields.String(description="gene product name/description", required=True,
            attribute=lambda x: extract_json_value(x.annotation, 'name')),
    'type': fields.String(description="gene type", required=True),
    'locus': fields.String(description="named locus", 
            attribute=lambda x: extract_json_value(x.annotation, 'location')),
    'start': fields.Integer(description="start coordinate for gene", required=True),
    'end': fields.Integer(description="end coordinate for gene", required=True),
    'chromosome': fields.String(description="chromosome on which gene is located", required=True),
    'strand': fields.String(description="strand: + or -",
            attribute=lambda x: '-' if x.is_reversed else '+'),
    'synonyms': fields.List(fields.String(), description="known synonyms (symbols) for gene")
}
