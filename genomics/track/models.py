''' GenomicsdB dataset (accession) data model '''
from sqlalchemy.orm import column_property
from shared_resources.db import db
from shared_resources.fields import GenomeBuild

def table(genomeBuild):
    """determine bind_db --> table based on genome_build route param"""
    bind_db = GenomeBuild().deserialize(genomeBuild)
    return Track_GRCh38 if bind_db == 'GRCh38' else Track_GRCh37

class TrackMixin:
    track = db.Column(db.String, primary_key=True)
    dataset_accession = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)
    attribution = db.Column(db.String)
    category = db.Column(db.String)
    subcategory =db.Column(db.String)
    
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


class Track_GRCh38(TrackMixin, db.Model):
    __bind_key__ = 'GRCh38'
    __tablename__ = 'trackattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('track')
    

class Track_GRCh37(TrackMixin, db.Model):
    __bind_key__ = 'GRCh37'
    __tablename__ = 'trackattributes'
    __table_args__ = {'schema': 'niagads', 'extend_existing':True}
    id = db.synonym('track')
