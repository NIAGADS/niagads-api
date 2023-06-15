from flask_restx import fields


gene_extended_properties = {
    'name': fields.String(description="gene product name/description", required=True,
            example="apolipoprotein E"),
            #attribute=lambda x: extract_json_value(x.annotation, 'name')),
    'type': fields.String(description="gene type", required=True, example="protein coding"),
    'locus': fields.String(description="named locus", example="19q13.32"),   
    'strand': fields.String(description="strand: + or -", example="+"),
    'synonyms': fields.List(fields.String(), description="known synonyms (symbols) for gene", 
            example=["AD2"])
}
          
