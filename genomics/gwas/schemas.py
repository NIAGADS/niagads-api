from flask_restx import fields
    
gwas_result = {
    'track': fields.String(description="unique identifier of track being queried", required=True),
    'variant_id': fields.String(description="variant identifier", attribute="metaseq_id", required=True),
    'ref_snp_id': fields.String(description="dbSNP refSnpID"),
    'pvalue': fields.String(description="pvalue, may be in scientific notation", required=True),
    'neg_log10_pvalue': fields.Float(description="-log10(pvalue)", required=True),
    'test_allele': fields.String(description="test allele in the GWAS analysis")
}
    
