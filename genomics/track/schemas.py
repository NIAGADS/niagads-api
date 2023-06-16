from flask_restx import fields

metadata = {
'attribution': fields.String(description="submitter or first author and date of publication", 
            required=True, 
            example="Wang et al. 2021"),
    'dataset_accession': fields.String(description="accession number for the track dataset",
            required=True),   
    'id': fields.String(required=True, 
            description="unique track identifiers", 
            example="NG00115_GRCh38_FEMALE")   
}
