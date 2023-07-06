''' GenomicsdB dataset (accession) data model '''
from sqlalchemy.orm import column_property
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import LtreeType

from shared_resources.db import db
from shared_resources.fields import GenomeBuild
from shared_resources import utils

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return TopGWAS_GRCh38 if bind_db == 'GRCh38' else TopGWAS_GRCh37


class GWASMixin:
    variant_gwas_top_hits_id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.String)
    metaseq_id = db.Column(db.String)
    ref_snp_id = db.Column(db.String)
    chromosome = db.Column(db.String)
    position = db.Column(db.Integer)
    is_adsp_variant = db.Column(db.Boolean)
    pvalue_display = db.Column(db.String)
    neg_log10_pvalue = db.Column(db.Float)
    test_allele = db.Column(db.String)
    # bin_index = db.Column(LtreeType)
    # display_attributes = db.Column(postgresql.JSONB)
    # annotation = db.Column(postgresql.JSONB)
    
    @property
    def variant(self):
        return self.ref_snp_id if self.ref_snp_id is not None else self.metaseq_id
    
    @property
    def start(self):
        return utils.to_numeric(self.display_attributes['location_start'])
    
    @property
    def end(self):
        return utils.to_numeric(self.display_attributes['location_end'])
    
    @property
    def span(self):
        return self.display_attributes['location_start'] + '-' + self.display_attributes['location_end']


class TopGWAS_GRCh38(GWASMixin, db.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'variantgwastophits'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    variant_id = db.synonym('metaseq_id')


class TopGWAS_GRCh37(GWASMixin, db.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'variantgwastophits'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    variant_id = db.synonym('metaseq_id')


# class GWAS_GRCh38(GWASMixin, db.Model):
#     __bind_key__ = 'GRCh38'
#     __tablename__ = 'variantgwas'
#     __table_args__ = {'schema': 'results', 'extend_existing':True}
    

# class GWAS_GRCh37(GWASMixin, db.Model):
#     __bind_key__ = 'GRCh37'
#     __tablename__ = 'variantgwas'
#     __table_args__ = {'schema': 'results', 'extend_existing':True}


def get_hits_by_variant(variant_id, genomeBuild):
    return 1