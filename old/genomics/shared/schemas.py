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

base_metadata = {
    'name': fields.String(required=True, 
            description="dataset name", 
            example="Genetic architecture of AD and differential effect between sexes"),
    'description': fields.String(required=True, 
            description="dataset description", 
            example="summary statistics from a sex-stratified genome-wide association study of SNPS from Alzheimer's Disease Genetics Consortium (ADGC) female samples with European ancestry. Subjects with individual-pairwise genetic relationship matrix (GRM) > 0.1 were excluded from analyses to ensure sample independence. Samples were selected from both ADGC phase 1 and phase 2 cohorts. (Lifted Over from GRCh37 to GRCh38)"),
    'data_source': fields.String(required=True, 
            description="source repository or data collection", 
            example="NIAGADS"),
    'type': fields.String(required=True, description="type of dataset or track", example="GWAS_sumstats"),
}

gene = {
    'name': fields.String(description="gene product name/description", required=True,
            example="apolipoprotein E"),
            #attribute=lambda x: extract_json_value(x.annotation, 'name')),
    'type': fields.String(description="gene type", required=True, example="protein coding"),
    'locus': fields.String(description="named locus", example="19q13.32"),   
    'strand': fields.String(description="strand: + or -", example="+"),
    'synonyms': fields.List(fields.String(), description="known synonyms (symbols) for gene", 
            example=["AD2"])
}
          
