from flask_restx import fields

phenotype = {
    'ancestry': fields.List(fields.String(), 
            description="population or 'ancestry' (from the Human Ancestry Ontology [HANCESTRO])",
            required=True),
    'race': fields.String(description="NIH Race Category"),
    'ethnicity': fields.String(description="NIH Ethnicity Category: Hispanic or Non-hispanic white"),
    'genotype': fields.String(description="APOE allele or APOE allele carrier status"),
    'disease': fields.List(fields.String(),
            description="disease, diagnosis or disease state"),
    'neuropathology': fields.List(fields.String(),
            description="neuropathology"),
    'biomarker': fields.String(description="Alzheimer's disease biomarker"),
    'biosample': fields.String(description="biosample type, usually blood or cerebrospinal fluid")
}

metadata = {
    'attribution': fields.String(description="submitter or first author and date of publication", 
            required=True, 
            attribute=lambda x: x.attribution.split('|')[0], 
            example="Wang et al. 2021"),
    'publication': fields.String(description="PubMED ID or DOI for primary publication", 
            attribute=lambda x: x.attribution.split('|')[1] if '|' in x.attribution else None,
            example="PMID:34122051"),
    'covariates': fields.List(fields.String(), 
            description="GWAS covariates or other adjustments made to a meta-analysis", 
            example= '["age","sex","population stratification"]'),
    'cohorts': fields.String()
}
