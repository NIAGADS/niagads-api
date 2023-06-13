from flask_restx import fields

metadata = {
    'name': fields.String(required=True, 
            description="dataset name", 
            example="Genetic architecture of AD and differential effect between sexes"),
    'description': fields.String(required=True, 
            description="dataset description", 
            example="summary statistics from a sex-stratified genome-wide association study of SNPS from Alzheimer's Disease Genetics Consortium (ADGC) female samples with European ancestry. Subjects with individual-pairwise genetic relationship matrix (GRM) > 0.1 were excluded from analyses to ensure sample independence. Samples were selected from both ADGC phase 1 and phase 2 cohorts. (Lifted Over from GRCh37 to GRCh38)"),
    'data_source': fields.String(required=True, default="NIAGADS",
            description="source repository or data collection", 
            example="NIAGADS"),
    'id': fields.String(required=True, 
            description="accession number in original data source", 
            example="NG00115")}


input_id = {
    'id': fields.String(required=True, 
        description="unique dataset identifier or accession number in original datasource"),
}
