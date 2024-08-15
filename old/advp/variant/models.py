''' ADVP variant data model '''
from sqlalchemy import select, func, column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects import postgresql

from shared_resources.db import db
from shared_resources.fields import GenomeBuild
from shared_resources import utils

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Variant_GRCh38 if bind_db == 'GRCh38' else Variant_GRCh37

class VariantMixin:
    variant_gwas_id = db.Column(db.String, primary_key=True)
    variant_record_primary_key = db.Column(db.String)
    bin_index = db.Column(db.String)
    neg_log10_pvalue = db.Column(db.String)
    pvalue_display= db.Column(db.String)
    frequency = db.Column(db.Float)
    metaseq_id = db.Column(db.String)
    ref_snp_id = db.Column(db.String)
    chromosome = db.Column(db.String)
    position = db.Column(db.Integer)
    # display_attributes = db.Column(postgresql.JSONB)
    is_adsp_variant = db.Column(db.Boolean)
    annotation = db.Column(postgresql.JSONB)
    restricted_stats = db.Column(postgresql.JSONB)
    test_allele = db.Column(db.String)
    population = db.Column(db.String)
    pubmed_id = db.Column(db.String)
    phenotype = db.Column(db.String)
    

class Variant_GRCh38(VariantMixin, db.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'advp'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('ref_snp_id')


class Variant_GRCh37(VariantMixin, db.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'advp'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('ref_snp_id')


def validate_variant(id, returnRecord=False, genomeBuild='GRCh38'):
    queryTable = table(genomeBuild)
    result = db.one_or_404(
            statement=db.session.query(queryTable).filter_by(id=id),
            description=f"No associations for the variant with refSNP ID '{id}' found in the NIAGADS ADVP.")
    return result if returnRecord else True
    
