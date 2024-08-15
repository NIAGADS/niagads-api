from flask_restx import fields

metadata = {
    'attribution': fields.String(description="submitter or first author and date of publication", 
            required=True, 
            example="Wang et al. 2021"),
    'collection': fields.String(description="accession number for the track dataset", attribute="dataset_accession",
            required=True),   
    'id': fields.String(required=True, 
            description="unique track identifiers", 
            example="NG00115_GRCh38_FEMALE")   ,
    'covariates': fields.List(fields.String(), 
            description="GWAS covariates or other adjustments made to a meta-analysis", 
            example= '["age","sex","population stratification"]'),
    'cohorts': fields.String()
}
