''' GenomicsdB gene data model '''
from shared_resources.db import db
from sqlalchemy import text, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import column_property

from shared_resources.fields import GenomeBuild
from shared_resources import utils


def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Gene_GRCh38 if bind_db == 'GRCh38' else Gene_GRCh37

class GeneMixin:
    source_id = db.Column(db.String, primary_key=True)
    gene_symbol = db.Column(db.String)
    gene_type = db.Column(db.String)
    location_start = db.Column(db.Integer)
    location_end = db.Column(db.Integer)
    chromosome = db.Column(db.String)
    is_reversed = db.Column(db.Boolean)
    transcript_count = db.Column(db.Integer)
    exon_count = db.Column(db.Integer)
    annotation = db.Column(postgresql.JSONB)

    @property
    def name(self):
        return utils.extract_json_value(self.annotation, 'name')
    
    @property
    def locus(self):
        return utils.extract_json_value(self.annotation, 'location')
    
    @property 
    def strand(self):
        return '-' if self.is_reversed else '+'
    
    @property
    def synonyms(self):
        if self.annotation is None:
            return None

        fields = ['prev_symbol', 'alias_symbol']
        aliases = '|'.join([a for a in [extract_json_value(self.annotation, f) for f in fields] if a is not None])
        
        return aliases.split('|')

    

class Gene_GRCh38(GeneMixin, db.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'geneattributes'
    __table_args__ = {'schema': 'cbil', 'extend_existing':True}
    id = db.synonym('source_id')
    type = db.synonym('gene_type')
    symbol = db.synonym('gene_symbol')
    start = db.synonym('location_start')
    end = db.synonym('location_end')

    
 
class Gene_GRCh37(GeneMixin, db.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'geneattributes'
    __table_args__ = {'schema': 'cbil', 'extend_existing':True}
    id = db.synonym('source_id')
    type = db.synonym('gene_type')
    symbol = db.synonym('gene_symbol')
    start = db.synonym('location_start')
    end = db.synonym('location_end')

