''' GenomicsdB dataset (accession) data model '''
from sqlalchemy.orm import column_property
from shared_resources.db import db
from shared_resources.fields import GenomeBuild

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return TopGWAS_GRCh38 if bind_db == 'GRCh38' else TopGWAS_GRCh37


class GWASMixin:
    variant_gwas_top_hits_id = db.Column(db.Integer, primary_key=True)



# select track, metaseq_id, ref_snp_id, chromosome, position, display_attributes,
# is_adsp_variant, bin_index, neg_log10_pvalue, annotation
# pvalue_display, test_allele from niagads.variantgwastophits;

# class GWAS_GRCh38(GWASMixin, db.Model):
#     __bind_key__ = 'GRCh38'
#     __tablename__ = 'variantgwas'
#     __table_args__ = {'schema': 'results', 'extend_existing':True}
    

# class GWAS_GRCh37(GWASMixin, db.Model):
#     __bind_key__ = 'GRCh37'
#     __tablename__ = 'variantgwas'
#     __table_args__ = {'schema': 'results', 'extend_existing':True}


class TopGWAS_GRCh38(GWASMixin, db.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'variantgwastophits'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('track')
    

class TopGWAS_GRCh37(GWASMixin, db.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'variantgwastophits'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('track')
