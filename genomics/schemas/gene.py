from flask_restx import fields
from shared_resources.utils import extract_json_value

def get_gene_synonyms(annotation):
    """extract gene synonyms from annotation field and return as list
        looks in 'prev_symbol', 'alias_symbol'

    Args:
        annotation (JSONB obejct): annotation JSONB field from the GeneAttributes table
    """
    if annotation is None:
        return None

    fields = ['prev_symbol', 'alias_symbol']
    aliases = '|'.join([a for a in [extract_json_value(annotation, f) for f in fields] if a is not None])
    
    return aliases.split('|')

    
    
# TODO link outs

gene = {
    'id': fields.String(description="Ensembl Identifier", required=True, example="ENSG00000130203"),
    'symbol': fields.String(description="Official gene symbol", required=True, example="APOE"),
    'name': fields.String(description="gene product name/description", required=True,
            example="apolipoprotein E",
            attribute=lambda x: extract_json_value(x.annotation, 'name')),
    'type': fields.String(description="gene type", required=True, example="protein coding"),
    'locus': fields.String(description="named locus", example="19q13.32",
            attribute=lambda x: extract_json_value(x.annotation, 'location')),
    'start': fields.Integer(description="start coordinate for gene", required=True, example=45409011),
    'end': fields.Integer(description="end coordinate for gene", required=True, example=45412650),
    'chromosome': fields.String(description="chromosome on which gene is located", required=True, example="chr19"),
    'strand': fields.String(description="strand: + or -",
            attribute=lambda x: '-' if x.is_reversed else '+', example="+"),
    'synonyms': fields.List(fields.String(), description="known synonyms (symbols) for gene", 
            example=["AD2"],
            attribute=lambda x: get_gene_synonyms(x.annotation))
}
