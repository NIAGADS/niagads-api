from flask_restx import fields

base = {
    'name': fields.String(required=True, description="dataset name", example="Genetic architecture of AD and differential effect between sexes"),
    'description': fields.String(required=True, description="dataset description", example="summary statistics from a sex-stratified genome-wide association study of SNPS from Alzheimer's Disease Genetics Consortium (ADGC) female samples with European ancestry. Subjects with individual-pairwise genetic relationship matrix (GRM) > 0.1 were excluded from analyses to ensure sample independence. Samples were selected from both ADGC phase 1 and phase 2 cohorts. (Lifted Over from GRCh37 to GRCh38)"),
    'data_source': fields.String(required=True, description="source repository or data collection", example="NIAGADS"),
    'id': fields.String(required=True, description="accession number in original data source", example="NG00115")}

filer = {'assay': fields.String(required=True, description="assay type"),
        'antibody_target': fields.String(description="antibody target in ChIP seq or other immunoprecipitation experiment")
        }

genomicsdb = {
    'attribution': fields.String(required=True, description="submitter or first author and date of publication", example="Wang et al. 2021"),
    'publication': fields.String("PubMED ID or DOI for primary publication", example="PMID:34122051")
}

genomicsdb_track = {
    'covariates': fields.String(description="GWAS covariates or other adjustments made to a meta-analysis", example="coming soon"),
    'phenotypes': fields.String(desciption="phenotypes", example="coming soon")
}