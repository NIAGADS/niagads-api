''' GenomicsdB gene data model '''
from shared_resources.db import genomicsdb as gdb
from sqlalchemy import text, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import column_property
from shared_resources.fields import GenomeBuild
from shared_resources.utils import extract_json_value


def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Gene_GRCh38 if bind_db == 'GRCh38' else Gene_GRCh37

class GeneMixin:
    source_id = gdb.Column(gdb.String, primary_key=True)
    gene_symbol = gdb.Column(gdb.String)
    gene_type = gdb.Column(gdb.String)
    location_start = gdb.Column(gdb.Integer)
    location_end = gdb.Column(gdb.Integer)
    chromosome = gdb.Column(gdb.String)
    is_reversed = gdb.Column(gdb.Boolean)
    transcript_count = gdb.Column(gdb.Integer)
    exon_count = gdb.Column(gdb.Integer)
    annotation = gdb.Column(postgresql.JSONB)

    @property
    def name(self):
        return extract_json_value(self.annotation, 'name')
    
    @property
    def locus(self):
        return extract_json_value(self.annotation, 'location')
    
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

    

class Gene_GRCh38(GeneMixin, gdb.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'geneattributes'
    __table_args__ = {'schema': 'cbil', 'extend_existing':True}
    id = gdb.synonym('source_id')
    type = gdb.synonym('gene_type')
    symbol = gdb.synonym('gene_symbol')
    start = gdb.synonym('location_start')
    end = gdb.synonym('location_end')

    
 
class Gene_GRCh37(GeneMixin, gdb.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'geneattributes'
    __table_args__ = {'schema': 'cbil', 'extend_existing':True}
    id = gdb.synonym('source_id')
    type = gdb.synonym('gene_type')
    symbol = gdb.synonym('gene_symbol')
    start = gdb.synonym('location_start')
    end = gdb.synonym('location_end')
