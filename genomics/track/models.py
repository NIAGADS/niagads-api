''' GenomicsdB dataset (accession) data model '''
from sqlalchemy.orm import column_property
from shared_resources.db import genomicsdb as gdb
from shared_resources.fields import GenomeBuild

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Track_GRCh38 if bind_db == 'GRCh38' else Track_GRCh37

class TrackMixin:
    track = gdb.Column(gdb.String, primary_key=True)
    dataset_accession = gdb.Column(gdb.String)
    name = gdb.Column(gdb.String)
    description = gdb.Column(gdb.String)
    attribution = gdb.Column(gdb.String)
    category = gdb.Column(gdb.String)
    subcategory =gdb.Column(gdb.String)
    
    @property
    def data_source(self):
        return "NIAGADS"
    
    @property
    def type(self):
        match self.subcategory:
            case "GWAS summary statistics":
                return "GWAS_sumstats"
            case _:
                return "GWAS_sumstats"


class Track_GRCh38(TrackMixin, gdb.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'trackattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = gdb.synonym('track')
    

class Track_GRCh37(TrackMixin, gdb.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'trackattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = gdb.synonym('track')
