from flask_restx import fields

metadata = {
    'attribution': fields.String(required=True, 
                                description="submitter or first author and date of publication", 
                                attribute=lambda x: x.attribution.split('|')[0], 
                                example="Wang et al. 2021"),
    'publication': fields.String("PubMED ID or DOI for primary publication", 
                                attribute=lambda x: x.attribution.split('|')[1] if '|' in x.attribution else None,
                                example="PMID:34122051"),
    'covariates': fields.String(description="GWAS covariates or other adjustments made to a meta-analysis", example="coming soon"),
    'phenotypes': fields.String(desciption="phenotypes", example="coming soon")
}
